-- Case 3: order total differs from items minus discount
SELECT o.id AS order_id, o.total_cents, SUM(i.qty * i.unit_cents) - o.discount_cents AS expected_cents,
       o.total_cents - (SUM(i.qty * i.unit_cents) - o.discount_cents) AS diff_cents
FROM orders o JOIN order_items i ON i.order_id = o.id
GROUP BY o.id HAVING diff_cents <> 0 ORDER BY o.id;
