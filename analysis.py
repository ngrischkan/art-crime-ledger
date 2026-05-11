import sqlite3
conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT c.nickname, SUM(jc.payout) as total_earned
    FROM job_crew jc
    JOIN crew c ON jc.crew_id = c.id
    GROUP BY c.nickname
    ORDER BY total_earned DESC
""")

rows = cursor.fetchall()

print(f"\n{'NICKNAME':<16} {'TOTAL EARNED'}")
print("-" * 85)

for row in rows:
    nickname, total_earned = row
    print(f"{nickname:<16} ${total_earned:,.0f}")

cursor.execute("""
    SELECT m.title, COUNT(*) as times_targeted
    FROM jobs j
    JOIN marks m ON j.mark_id = m.id
    GROUP BY m.title
    ORDER BY times_targeted DESC
""")

rows = cursor.fetchall()

print(f"\n{'TITLE':<45} {'COUNT'}")
print("-" * 85)

for row in rows:
    title, count = row
    print(f"{title:<45} {count}")

cursor.execute("""
    SELECT m.location,
        COUNT(*) as total_jobs,
        SUM(CASE WHEN j.outcome = 'clean' THEN 1 ELSE 0 END) as clean_jobs,
        ROUND(100.0 * SUM(CASE WHEN j.outcome = 'clean' THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate
    FROM jobs j
    JOIN marks m ON j.mark_id = m.id
    GROUP BY m.location
    ORDER BY success_rate DESC
""")

rows = cursor.fetchall()

print(f"\n{'LOCATION':<25} {'JOBS':<7} {'CLEAN':<7} {'SUCCESS RATE'}")
print("-" * 85)

for row in rows:
    location, total_jobs, clean_jobs, success_rate = row
    print(f"{location:<25} {total_jobs:<7} {clean_jobs:<7} {success_rate}%")

conn.close()
