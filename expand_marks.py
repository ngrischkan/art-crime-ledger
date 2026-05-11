import sqlite3

conn = sqlite3.connect("ledger.db")
cursor = conn.cursor()

def assign_difficulty(museum, estimated_value):
    if museum == "Louvre" or museum == "Musée d'Orsay":
        base = 8
    elif museum == "Centre Pompidou" or museum == "Musée de l'Orangerie" or museum == "Musée Picasso":
        base = 6
    elif museum == "Musée Rodin" or museum == "Musée Marmottan Monet" or museum == "Musée Jacquemart-André" or museum == "Musée de Cluny":
        base = 4
    else:
        base = 2  # private galleries, auction houses, unknown

    if estimated_value >= 500_000_000:
        base += 2
    elif estimated_value >= 100_000_000:
        base += 1

    return min(base, 10)

marks = [
    # Louvre
    ("The Wedding Feast at Cana", "Paolo Veronese", 1563, "Louvre", 450_000_000.0),
    ("Virgin of the Rocks", "Leonardo da Vinci", 1483, "Louvre", 320_000_000.0),
    ("The Coronation of Napoleon", "Jacques-Louis David", 1807, "Louvre", 180_000_000.0),
    ("Winged Victory of Samothrace", "Unknown", -190, "Louvre", 250_000_000.0),
    ("The Lacemaker", "Johannes Vermeer", 1669, "Louvre", 160_000_000.0),

    # Musée d'Orsay
    ("Starry Night Over the Rhône", "Vincent van Gogh", 1888, "Musée d'Orsay", 200_000_000.0),
    ("Olympia", "Édouard Manet", 1863, "Musée d'Orsay", 180_000_000.0),
    ("Dance at Le Moulin de la Galette", "Pierre-Auguste Renoir", 1876, "Musée d'Orsay", 250_000_000.0),
    ("The Gleaners", "Jean-François Millet", 1857, "Musée d'Orsay", 90_000_000.0),
    ("Whistler's Mother", "James McNeill Whistler", 1871, "Musée d'Orsay", 75_000_000.0),

    # Centre Pompidou
    ("The Red Studio", "Henri Matisse", 1911, "Centre Pompidou", 120_000_000.0),
    ("Composition II in Red Blue and Yellow", "Piet Mondrian", 1930, "Centre Pompidou", 80_000_000.0),

    # Musée de l'Orangerie
    ("Water Lilies — Morning", "Claude Monet", 1916, "Musée de l'Orangerie", 180_000_000.0),
    ("Paul Guillaume as Novo Pilota", "Amedeo Modigliani", 1915, "Musée de l'Orangerie", 60_000_000.0),

    # Musée Picasso
    ("Self-Portrait", "Pablo Picasso", 1907, "Musée Picasso", 90_000_000.0),
    ("The Kiss", "Pablo Picasso", 1969, "Musée Picasso", 55_000_000.0),

    # Musée Rodin
    ("The Kiss", "Auguste Rodin", 1882, "Musée Rodin", 25_000_000.0),
    ("The Gates of Hell", "Auguste Rodin", 1917, "Musée Rodin", 40_000_000.0),

    # Musée Marmottan Monet
    ("The Magpie", "Claude Monet", 1869, "Musée Marmottan Monet", 35_000_000.0),
    ("Impression Sunrise", "Claude Monet", 1872, "Musée Marmottan Monet", 80_000_000.0),

    # Musée de Cluny
    ("The Lady and the Unicorn — Sight", "Unknown", 1500, "Musée de Cluny", 30_000_000.0),
    ("The Lady and the Unicorn — Desire", "Unknown", 1500, "Musée de Cluny", 30_000_000.0),

    # Private Galleries
    ("Femme à la Montre", "Pablo Picasso", 1932, "Galerie Perrotin", 120_000_000.0),
    ("Le Repos", "Henri Matisse", 1922, "Galerie Kamel Mennour", 18_000_000.0),
]

for mark in marks:
    title, artist, year, museum, value = mark
    difficulty = assign_difficulty(museum, value)
    cursor.execute("""
        INSERT INTO marks (title, artist, year_created, location, estimated_value, security_difficulty)        
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, artist, year, museum, value, difficulty))

conn.commit()
print(f"Added {len(marks)} marks to the database.")
conn.close()