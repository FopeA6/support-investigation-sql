-- Case 1: same payment event recorded more than once
SELECT order_id, event_id, COUNT(*) AS times_recorded, SUM(amount_cents) AS booked_cents
FROM payments GROUP BY order_id, event_id HAVING COUNT(*) > 1 ORDER BY order_id;
