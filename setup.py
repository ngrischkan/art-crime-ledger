import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

# Create the crew table
cursor.execute("""
CREATE TABLE IF NOT EXISTS crew (
    crew_id INTEGER PRIMARY KEY,
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
    mark_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    year_created INTEGER,
    location TEXT NOT NULL,
    estimated_value REAL NOT NULL,
    security_difficulty INTEGER DEFAULT 1,
    status TEXT DEFAULT 'untouched'                  
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    job_id INTEGER PRIMARY KEY,
    mark_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    outcome TEXT NOT NULL,
    gross_take REAL NOT NULL,
    expenses REAL NOT NULL DEFAULT 0,
    net_profit REAL,
    notes TEXT,
    FOREIGN KEY (mark_id) REFERENCES marks(mark_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS job_crew (
    job_id INTEGER NOT NULL,
    crew_id INTEGER NOT NULL,
    role_on_job TEXT NOT NULL,
    payout REAL NOT NULL,
    PRIMARY KEY (job_id, crew_id),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (crew_id) REFERENCES crew(crew_id)
)
""")

conn.commit()
conn.close()

print("Database created.")