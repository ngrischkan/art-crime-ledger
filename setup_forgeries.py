import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

# Create the forgeries table
cursor.execute("""
CREATE TABLE IF NOT EXISTS forgeries (
    forgery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mark_id INTEGER,
    forger_id INTEGER,
    date_completed TEXT,
    sale_price REAL,
    buyer TEXT,
    detected INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (mark_id) REFERENCES marks(mark_id),
    FOREIGN KEY (forger_id) REFERENCES crew(crew_id)
)
""")

conn.commit()
conn.close()

print("Database created.")
