# Case 5: Daily report shows different order counts from the dashboard
**Classification:** expected behaviour (time zone), documentation and enablement issue.
**Impact:** 10 orders appear on a different day depending on whether the report uses UTC or UTC+1.
**Repro:** `python run.py sql/05_day_boundary.sql`. All affected orders were placed between 23:00 and 23:59 UTC.
**Root-cause hypothesis:** the dashboard groups by UTC date and the daily report by local time. Neither is wrong.
**Action:** document which time zone each report uses and make it visible on the report. No code change needed.
