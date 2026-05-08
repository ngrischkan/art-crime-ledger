import sqlite3

conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

# Pull all crew members, ordered by skill (highest first)
cursor.execute("""
    SELECT nickname, real_name, age, role, skill, heat
    FROM crew
    ORDER BY skill DESC
""")

rows = cursor.fetchall()

print(f"\n{'NICKNAME':<15} {'REAL NAME':<28} {'AGE':<5} {'ROLE':<20} {'SKILL':<7} {'HEAT'}")
print("-" * 85)

for row in rows:
    nickname, real_name, age, role, skill, heat = row
    print(f"{nickname:<15} {real_name:<28} {age:<5} {role:<20} {skill:<7} {heat}")

conn.close()