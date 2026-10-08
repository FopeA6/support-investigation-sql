# Case 4: Carrier is collecting parcels for orders that do not exist
**Classification:** data integrity issue.
**Impact:** 3 shipments point to orders that were deleted.
**Repro:** `python run.py sql/04_orphan_shipments.sql`.
**Root-cause hypothesis:** deleting an order does not cancel or delete its shipment, and nothing enforces the link (`shipments.order_id` has no foreign key).
**Action:** cancel the 3 shipments with the carrier. Ask Engineering to add the foreign key or make deletion cancel the shipment.
