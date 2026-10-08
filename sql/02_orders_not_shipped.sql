-- Case 2: paid orders with no shipment, grouped by customer country and sync result
SELECT c.country, s.result, s.detail, COUNT(*) AS orders
FROM orders o JOIN customers c ON c.id = o.customer_id
JOIN sync_log s ON s.order_id = o.id AND s.target = 'warehouse'
LEFT JOIN shipments sh ON sh.order_id = o.id
WHERE o.status = 'paid' AND sh.id IS NULL
GROUP BY c.country, s.result, s.detail;
