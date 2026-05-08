import sqlite3

conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

marks = [
    ("Mona Lisa", "Leonardo da Vinci", 1503, "Louvre", 900_000_000.0, 10),
    ("The Wedding Feast at Cana", "Paolo Veronese", 1563, "Louvre", 450_000_000.0, 10),
    ("Water Lilies", "Claude Monet", 1916, "Musee de l'Orangerie", 200_000_000.0, 9),
    ("Impression, Sunrise", "Claude Monet", 1872, "Musee Marmottan Monet", 80_000_000.0, 5),
    ("Guernica", "Pablo Picasso", 1937, "Musee Picasso", 40_000_000.0, 6),
    ("The Thinker", "Auguste Rodin", 1904, "Musee Rodin", 15_000_000.0, 6)
]

cursor.executemany("""
    INSERT INTO marks (title, artist, year_created, location, estimated_value, security_difficulty)
    VALUES (?, ?, ?, ?, ?, ?) 
""", marks)

conn.commit()

cursor.execute("SELECT COUNT(*) FROM marks")
count = cursor.fetchone()[0]
print(f"Marks table now has {count} pieces.")

conn.close()