import sqlite3

conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT title, artist, location, estimated_value, security_difficulty, status
    FROM marks
    ORDER BY security_difficulty DESC
""")

rows = cursor.fetchall()

print(f"{'TITLE':<28} {'ARTIST':<22} {'LOCATION':<25} {'VALUE':<16} {'DIFF':<6} {'STATUS'}")
print("-" * 105)

for row in rows:
    title, artist, location, estimated_value, security_difficulty, status = row
    print(f"{title:<28} {artist:<22} {location:<25} ${estimated_value:<15,.0f} {security_difficulty:<6} {status}")

conn.close()