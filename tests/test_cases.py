import os, sqlite3, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import seed

ROOT = os.path.join(os.path.dirname(__file__), "..")
def q(name):
    seed.build(os.path.join(ROOT, "test.db"))
    db = sqlite3.connect(os.path.join(ROOT, "test.db"))
    return db.execute(open(os.path.join(ROOT, "sql", name)).read()).fetchall()

class Cases(unittest.TestCase):
    def test_duplicate_payments(self): self.assertEqual([r[0] for r in q("01_duplicate_payments.sql")], [10, 25, 40, 55, 70, 85])
    def test_us_orders_not_shipped(self):
        rows = q("02_orders_not_shipped.sql"); self.assertEqual(len(rows), 1); self.assertEqual(rows[0][0], "US"); self.assertEqual(rows[0][2], "no warehouse for country US")
    def test_total_mismatch(self): self.assertEqual([r[0] for r in q("03_total_mismatch.sql")], [15, 30, 45, 60]); self.assertTrue(all(r[3] == 37 for r in q("03_total_mismatch.sql")))
    def test_orphan_shipments(self): self.assertEqual([r[1] for r in q("04_orphan_shipments.sql")], [90, 91, 92])
    def test_day_boundary(self): self.assertTrue({100, 101, 102, 103} <= {r[0] for r in q("05_day_boundary.sql")})
    def tearDown(self):
        p = os.path.join(ROOT, "test.db")
        if os.path.exists(p): os.remove(p)
if __name__ == "__main__": unittest.main()
