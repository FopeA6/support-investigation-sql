"""Builds a deterministic, synthetic SQLite database with five planted problems.
Run: python seed.py  ->  support.db
"""
import random, sqlite3, os
from datetime import datetime, timedelta

def build(path="support.db"):
    if os.path.exists(path): os.remove(path)
    db = sqlite3.connect(path)
    db.executescript(open(os.path.join(os.path.dirname(__file__) or ".", "schema.sql")).read())
    rnd = random.Random(7)
    countries = ["GB"] * 5 + ["US"] * 4 + ["DE", "NG"]
    for i in range(1, 61):
        db.execute("INSERT INTO customers VALUES (?,?,?)", (i, f"user{i}@example.com", rnd.choice(countries)))
    # config: the warehouse map is missing US (planted config problem, case 2)
    db.executemany("INSERT INTO integration_config VALUES (?,?)",
                   [("warehouse_map", "GB:LDN,DE:LDN,NG:LDN"), ("shipping_enabled", "true")])
    base = datetime(2026, 9, 1)
    oid = pid = sid = iid = lid = 0
    country = {r[0]: r[1] for r in db.execute("SELECT id, country FROM customers")}
    for n in range(1, 201):
        oid += 1
        cust = rnd.randint(1, 60)
        created = base + timedelta(hours=rnd.randint(0, 24 * 28), minutes=rnd.randint(0, 59))
        items = [(rnd.choice(["TOTE", "SCARF", "CLUTCH"]), rnd.randint(1, 2), rnd.choice([2500, 4000, 8500])) for _ in range(rnd.randint(1, 3))]
        subtotal = sum(q * u for _, q, u in items)
        discount = 0
        total = subtotal
        db.execute("INSERT INTO orders VALUES (?,?,?,?,?,?)", (oid, cust, "paid", total, discount, created.isoformat()))
        for sku, q, u in items:
            iid += 1; db.execute("INSERT INTO order_items VALUES (?,?,?,?,?)", (iid, oid, sku, q, u))
        pid += 1; db.execute("INSERT INTO payments VALUES (?,?,?,?,?)", (pid, oid, f"evt_{oid}", total, (created + timedelta(minutes=1)).isoformat()))
        # normal sync: shipment created, except US orders (case 2: no warehouse mapping)
        if country[cust] == "US":
            lid += 1; db.execute("INSERT INTO sync_log VALUES (?,?,?,?,?)", (lid, oid, "warehouse", "skipped", "no warehouse for country US"))
        else:
            sid += 1; db.execute("INSERT INTO shipments VALUES (?,?,?,?)", (sid, oid, "RM", (created + timedelta(hours=6)).isoformat()))
            lid += 1; db.execute("INSERT INTO sync_log VALUES (?,?,?,?,?)", (lid, oid, "warehouse", "ok", None))
    # case 1: duplicate payment webhooks (same event_id delivered twice) for 6 orders
    for o in (10, 25, 40, 55, 70, 85):
        a, t = db.execute("SELECT amount_cents, received_at FROM payments WHERE order_id=?", (o,)).fetchone()
        pid += 1; db.execute("INSERT INTO payments VALUES (?,?,?,?,?)", (pid, o, f"evt_{o}", a, t))
    # case 3: order totals that do not equal items minus discount (rounding on discounted orders)
    for o in (15, 30, 45, 60):
        db.execute("UPDATE orders SET discount_cents=1000, total_cents=total_cents-1000+37 WHERE id=?", (o,))
    # case 4: orphaned shipments (order deleted but shipment remains)
    for o in (90, 91, 92):
        db.execute("DELETE FROM payments WHERE order_id=?", (o,)); db.execute("DELETE FROM order_items WHERE order_id=?", (o,)); db.execute("DELETE FROM orders WHERE id=?", (o,))
    # case 5: orders created 23:00-23:59 UTC are reported on the wrong day by a daily report in UTC+1
    for k, o in enumerate((100, 101, 102, 103)):
        db.execute("UPDATE orders SET created_at=? WHERE id=?", (datetime(2026, 9, 10 + k, 23, 30).isoformat(), o))
    db.commit(); db.close()

if __name__ == "__main__":
    build(); print("built support.db")
