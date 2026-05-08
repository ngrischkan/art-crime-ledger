import sqlite3

# Open connection to the existing database
conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

# Each tuple is one crew member, in this order:
# (nickname, real_name, age, role, nationality, skill, cut_percentage, heat)
crew_members = [
    ("Saunière",      "Étienne Marchand",        58, "Mastermind",          "French",          9, 0.18, 1),
    ("Bridger",       "Hendrik Vos",             49, "Vault/Security",      "Dutch",           9, 0.15, 0),
    ("Handsome Rob",  "Robert Whitfield-Mensah", 36, "Social Engineer",     "British",         7, 0.11, 2),
    ("Baby",          "Camille Roussel",         27, "Getaway Driver",      "French",          8, 0.10, 1),
    ("The Critic",    "Margarethe Lindqvist",    62, "Authentication",      "Swedish",         8, 0.10, 0),
    ("Le Chaos",      "Mathieu Brun",            31, "Disruption",          "French",          6, 0.08, 3),
    ("Rook",          "Tomasz Wójcik",           34, "Field Operative",     "Polish",          7, 0.10, 1),
    ("Courier Zero",  "Yusra Haddad",            41, "Transport",           "Lebanese-French", 8, 0.10, 0),
    ("The Cleaner",   "Anouk Vandenberg",        44, "Evidence Removal",    "Belgian",         8, 0.08, 0),
]

# Insert all of them at once using executemany
cursor.executemany("""
    INSERT INTO crew (nickname, real_name, age, role, nationality, skill, cut_percentage, heat)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", crew_members)

conn.commit()

# Quick sanity check: count the rows we just inserted
cursor.execute("SELECT COUNT(*) FROM crew")
count = cursor.fetchone()[0]
print(f"Crew table now has {count} members.")

conn.close()