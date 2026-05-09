import sqlite3

# Open connection to the existing database
conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO jobs (mark_id, date, outcome, gross_take, expenses, notes)
    VALUES (?, ?, ?, ?, ?, ?)
""", (6, "2023-08-25", "clean", 14_500_000.0, 450_000.0, "Wednesday night, 2:14 AM. Handsome Rob's asset called in sick on schedule. Rook had the bronze out the side door in under nine minutes. Baby made the handoff at Porte de Vincennes; Courier Zero had the piece across the Belgian border by sunrise."))
new_job_id = cursor.lastrowid

job_crew_rows = [
    (new_job_id, 1, "planner", 2_610_000.0),
    (new_job_id, 3, "inside access", 1_595_000.0),
    (new_job_id, 7, "extractor", 1_450_000.0),
    (new_job_id, 4, "primary driver", 1_450_000.0),
    (new_job_id, 8, "transport", 1_450_000.0),
    (new_job_id, 9, "site sanitization", 1_160_000.0)
]

cursor.executemany("""
    INSERT INTO job_crew (job_id, crew_id, role_on_job, payout)
    VALUES (?, ?, ?, ?)
""", job_crew_rows)

cursor.execute("UPDATE jobs SET net_profit = ? WHERE id = ?", (4_335_000.0, new_job_id))

conn.commit()

cursor.execute("SELECT id, mark_id, date, outcome, gross_take, net_profit FROM jobs WHERE id = ?", (new_job_id,))
print("Job recorded:", cursor.fetchone())

cursor.execute("SELECT crew_id, role_on_job, payout FROM job_crew WHERE job_id = ? ORDER BY payout DESC", (new_job_id,))
print("Crew payouts:")
for row in cursor.fetchall():
    print(" ", row)

conn.close()