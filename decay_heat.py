import sqlite3

conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

cursor.execute("UPDATE crew SET heat = MAX(0, heat - 1)")
conn.commit()

cursor.execute("SELECT nickname, heat FROM crew ORDER BY heat DESC")
for nickname, heat in cursor.fetchall():
    print(f"{nickname:<16} heat={heat}")

conn.close()
