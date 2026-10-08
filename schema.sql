-- Synthetic data only. A small store whose orders sync to a shipping integration.
CREATE TABLE customers (id INTEGER PRIMARY KEY, email TEXT NOT NULL, country TEXT NOT NULL);
CREATE TABLE orders (
  id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id),
  status TEXT NOT NULL, total_cents INTEGER NOT NULL, discount_cents INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL            -- UTC, ISO 8601
);
CREATE TABLE order_items (id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(id), sku TEXT NOT NULL, qty INTEGER NOT NULL, unit_cents INTEGER NOT NULL);
CREATE TABLE payments (id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(id), event_id TEXT NOT NULL, amount_cents INTEGER NOT NULL, received_at TEXT NOT NULL);
CREATE TABLE shipments (id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, carrier TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE sync_log (id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, target TEXT NOT NULL, result TEXT NOT NULL, detail TEXT);
CREATE TABLE integration_config (key TEXT PRIMARY KEY, value TEXT NOT NULL);
