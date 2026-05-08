import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

# Create the crew table
cursor.execute("""
CREATE TABLE IF NOT EXISTS crew (
    id INTEGER PRIMARY KEY,
    nickname TEXT NOT NULL,
    real_name TEXT NOT NULL,
    age INTEGER,
    role TEXT,
    nationality TEXT,
    skill INTEGER,
    cut_percentage REAL,
    heat INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    year_created INTEGER,
    location TEXT NOT NULL,
    estimated_value REAL NOT NULL,
    security_difficulty INTEGER DEFAULT 1,
    status TEXT DEFAULT 'untouched'                  
)
""")

conn.commit()
conn.close()

print("Database created. Crew table ready.")