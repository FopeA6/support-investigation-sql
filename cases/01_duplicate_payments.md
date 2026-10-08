# Case 1: Customer says they were charged twice
**Classification:** product defect (likely missing idempotency), not a customer or config problem.
**Impact:** 6 of 200 orders have the same payment event booked twice; booked revenue is overstated by the amount of each duplicate.
**Repro:** `python run.py sql/01_duplicate_payments.sql`. Each affected order has one `event_id` recorded twice with identical amounts and timestamps.
**Evidence:** same `event_id`, same amount, same `received_at`, so a redelivered webhook rather than two real charges.
**Root-cause hypothesis:** the payment webhook handler inserts on every delivery and does not check `event_id` first.
**Handoff to Engineering:** add a unique constraint on `event_id` and make the handler idempotent. Support action in the meantime: confirm with the payment provider that the customer was charged once, and tell the customer.
