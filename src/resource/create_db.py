import sqlite3
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/resources.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS resources (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        type        TEXT NOT NULL,
        lat         REAL NOT NULL,
        lon         REAL NOT NULL,
        address     TEXT,
        phone       TEXT,
        description TEXT,
        city        TEXT
    )
''')

# Sample data — Pune city
resources = [
    # Hospitals
    ("Sassoon General Hospital",    "hospital", 18.5167, 73.8567, "Pune", "+91-20-26128000", "Government hospital", "Pune"),
    ("Ruby Hall Clinic",            "hospital", 18.5284, 73.8845, "Wanowrie Rd", "+91-20-66455000", "Private hospital", "Pune"),
    ("KEM Hospital",                "hospital", 18.5314, 73.8446, "Sardar Moodliar Rd", "+91-20-26125600", "Government hospital", "Pune"),
    ("Jehangir Hospital",           "hospital", 18.5248, 73.8764, "32 Sassoon Rd", "+91-20-66814444", "Private hospital", "Pune"),
    ("Poona Hospital",              "hospital", 18.5196, 73.8553, "27 Sadashiv Peth", "+91-20-24330011", "Private hospital", "Pune"),

    # Water points
    ("PMC Water Station - Swargate","water",    18.5018, 73.8587, "Swargate", None, "24/7 drinking water", "Pune"),
    ("Water ATM - Hadapsar",        "water",    18.5050, 73.9259, "Hadapsar", None, "Clean drinking water", "Pune"),
    ("Water Point - Shivajinagar",  "water",    18.5308, 73.8474, "Shivajinagar", None, "Municipal water point", "Pune"),

    # Shelters
    ("Red Cross Shelter - Pune",    "shelter",  18.5204, 73.8567, "Bund Garden Rd", "+91-20-26361883", "Emergency shelter", "Pune"),
    ("Night Shelter - Yerawada",    "shelter",  18.5524, 73.8917, "Yerawada", None, "Free night shelter", "Pune"),
    ("Relief Camp - Hadapsar",      "shelter",  18.4961, 73.9285, "Hadapsar", None, "Flood relief camp", "Pune"),

    # NGOs
    ("Jan Sahas Foundation",        "ngo",      18.5204, 73.8567, "Deccan Gymkhana", "+91-734-2423232", "Migrant worker support", "Pune"),
    ("iCall Mental Health",         "ngo",      18.5500, 73.8333, "TISS Pune", "+91-9152987821", "Mental health support", "Pune"),
    ("Smile Foundation",            "ngo",      18.5120, 73.8456, "Pune Camp", "+91-11-43123700", "Child & family support", "Pune"),

    # Food
    ("Akshaya Patra - Pune",        "food",     18.5089, 73.8116, "Pimpri", "+91-20-27442001", "Free meals distribution", "Pune"),
    ("Gurudwara Langar",            "food",     18.5169, 73.8553, "Pune Camp", None, "Free food 24/7", "Pune"),
    ("Feeding India",               "food",     18.5204, 73.8667, "Koregaon Park", "+91-9999123456", "Food distribution NGO", "Pune"),
]

cursor.executemany('''
    INSERT INTO resources (name, type, lat, lon, address, phone, description, city)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', resources)

conn.commit()
conn.close()

print(f"✅ Database created with {len(resources)} resources!")
print("   Types: hospital, water, shelter, ngo, food")