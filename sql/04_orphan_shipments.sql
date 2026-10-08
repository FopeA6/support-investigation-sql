-- Case 4: shipments whose order no longer exists
SELECT s.id AS shipment_id, s.order_id, s.carrier FROM shipments s
LEFT JOIN orders o ON o.id = s.order_id WHERE o.id IS NULL ORDER BY s.id;
