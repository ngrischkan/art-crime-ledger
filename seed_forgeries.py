import sqlite3

# Open connection to the existing database
conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

# Each tuple is one forgery, in this order:
# (mark_id, forger_id, date_completed, sale_price, buyer, detected, notes)
#
# mark_id references marks seeded by expand_marks.py (insertion order):
#   5  = The Lacemaker, Vermeer, Louvre, $160M
#   9  = The Gleaners, Millet, Musée d'Orsay, $90M
#   10 = Whistler's Mother, Whistler, Musée d'Orsay, $75M
#   20 = Impression Sunrise, Monet, Musée Marmottan Monet, $80M
#   24 = Le Repos, Matisse, Galerie Kamel Mennour, $18M
#
# forger_id 5 = The Critic (Margarethe Lindqvist) — Authentication
forgeries = [
    (5,  5, "2023-04-07", 1_400_000.0, "H. Vanthorpe",    0, "Vermeer panel, aged correctly. Vanthorpe doesn't ask questions."),
    (20, 5, "2023-09-18",   920_000.0, "P. Ferraro",       1, "Craquelure inconsistency flagged by Basel restorer. Ferraro is contained."),
    (9,  5, "2024-03-11",   760_000.0, "Anon.",            0, "Chain through Monaco. No blowback."),
    (10, 5, "2024-07-03",   610_000.0, "Anon.",            0, "American buyer via London intermediary. Sentimental value did the selling."),
    (24, 5, "2024-10-21",   185_000.0, "Private estate",   0, "Small-ticket. Gallery staff never noticed the swap."),
]

# Insert all of them at once using executemany
cursor.executemany("""
    INSERT OR IGNORE INTO forgeries (mark_id, forger_id, date_completed, sale_price, buyer, detected, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", forgeries)

conn.commit()

# Quick sanity check: count the rows we just inserted
cursor.execute("SELECT COUNT(*) FROM forgeries")
count = cursor.fetchone()[0]
print(f"Forgeries table now has {count} entries.")

conn.close()
