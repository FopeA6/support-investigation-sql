"""Run one investigation query: python run.py sql/01_duplicate_payments.sql"""
import sqlite3, sys
db = sqlite3.connect("support.db")
cur = db.execute(open(sys.argv[1]).read())
print(" | ".join(d[0] for d in cur.description))
for row in cur.fetchall(): print(" | ".join(str(x) for x in row))
