import sqlite3

conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

# --- ZONE 1: SQL query 1 ---
cursor.execute("""
    SELECT j.id, j.date, j.outcome, j.gross_take, j.net_profit,
           m.title, m.artist, m.location
    FROM jobs j
    JOIN marks m ON j.mark_id = m.id
""")
job_rows = cursor.fetchall()

# --- ZONE 2: Python loop ---
for job in job_rows:
    job_id, date, outcome, gross_take, net_profit, title, artist, location = job
    
    # Print the job header here (use an f-string)
    print(f"JOB #{job_id} | {date} | {outcome}")
    # Print the mark info here (use an f-string)
    print(f"Mark: {title} ({artist}) - {location}")
    # Print the take here (use an f-string with :,.0f for money)
    print(f"Take: ${gross_take:,.0f} gross / ${net_profit:,.0f} net")

    # --- ZONE 1 again: SQL query 2 ---
    cursor.execute("""
        SELECT c.nickname, jc.role_on_job, jc.payout
        FROM job_crew jc
        JOIN crew c ON jc.crew_id = c.id
        WHERE jc.job_id = ?
        ORDER BY jc.payout DESC
    """, (job_id,))
    crew_rows = cursor.fetchall()
    
    # --- ZONE 2 again: Python loop over crew ---
    print("  Crew:")
    for crew_row in crew_rows:
        nickname, role, payout = crew_row
        # Print each crew member here (use an f-string)
        print(f"  {nickname:<16} {role:<22} ${payout:,.0f}")
conn.close()