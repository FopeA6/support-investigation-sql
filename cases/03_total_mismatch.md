# Case 3: Order totals do not match the items
**Classification:** product defect (calculation).
**Impact:** 4 orders are 37 cents over what the items minus discount add up to.
**Repro:** `python run.py sql/03_total_mismatch.sql`. All four orders have a discount applied; no order without a discount is affected.
**Root-cause hypothesis:** rounding when the discount is applied, because the difference is the same small amount each time and only on discounted orders.
**Handoff to Engineering:** include the order ids, the formula expected, and the pattern (discounted orders only). Ask them to confirm how discounts are rounded.
