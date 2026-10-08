-- Case 5: orders whose UTC date differs from their UTC+1 (Europe/London summer) date
SELECT id AS order_id, created_at, date(created_at) AS utc_day, date(created_at, '+1 hour') AS local_day
FROM orders WHERE date(created_at) <> date(created_at, '+1 hour') ORDER BY id;
