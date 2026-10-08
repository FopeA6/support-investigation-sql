# Case 2: US customers say their paid orders never shipped
**Classification:** configuration, not a code defect. No Engineering escalation needed.
**Impact:** 56 paid orders, all to US customers, have no shipment.
**Repro:** `python run.py sql/02_orders_not_shipped.sql`. Every unshipped order is a US order with sync result `skipped` and detail "no warehouse for country US".
**Evidence:** `integration_config.warehouse_map` is `GB:LDN,DE:LDN,NG:LDN`. There is no US entry, and no other country is affected.
**Root-cause hypothesis:** the integration was set up before US sales began and the map was never extended.
**Action:** add a US warehouse mapping, then re-run the sync for the 56 skipped orders. Add a check that alerts when a country has orders but no mapping.
