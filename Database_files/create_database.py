import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect("App Version 1/food_tracker.db")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Create `user` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    uid INTEGER PRIMARY KEY,
    username TEXT,
    preferences TEXT,
    allergens TEXT,
    calorie_goal FLOAT,
    protein_goal FLOAT
);
""")

# Create `common_meal` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS common_meal (
    meal_id INTEGER PRIMARY KEY,
    meal TEXT,
    allergens TEXT,
    calories FLOAT,
    protein FLOAT,
    fats FLOAT,
    carbohydrates FLOAT,
    average_rating FLOAT
);
""")

# Create `food_log` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS food_log (
    log_id INTEGER PRIMARY KEY,
    meal_id INTEGER,
    date TIMESTAMP,
    uid INTEGER,
    meal_type TEXT CHECK(meal_type IN ('Breakfast', 'Lunch', 'Dinner', 'Snack')),
    food_name TEXT,
    calories FLOAT,
    protein FLOAT,
    fats FLOAT,
    carbohydrates FLOAT,
    FOREIGN KEY (uid) REFERENCES user(uid),
    FOREIGN KEY (meal_id) REFERENCES common_meal(meal_id)
);
""")

# Add a new column 'location_id' with a default value of 'Unknown'
cursor.execute("""
    ALTER TABLE food_log ADD COLUMN location_id TEXT DEFAULT 'Unknown'
""")

# Create `rating` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS rating (
    rating_id INTEGER PRIMARY KEY,
    meal_id INTEGER,
    uid INTEGER,
    rating INTEGER,
    FOREIGN KEY (meal_id) REFERENCES common_meal(meal_id),
    FOREIGN KEY (uid) REFERENCES user(uid)
);
""")

# Create `cafe_hoop` table
cursor.execute('''
CREATE TABLE IF NOT EXISTS cafe_hoop (
    name TEXT PRIMARY KEY,
    calories REAL,
    fat REAL,
    protein REAL,
    carbohydrates REAL,
    ingredients_text TEXT
)
''')

# Create `el_table` table
cursor.execute('''
CREATE TABLE IF NOT EXISTS el_table (
    name TEXT PRIMARY KEY,
    calories REAL,
    fat REAL,
    protein REAL,
    carbohydrates REAL,
    ingredients_text TEXT
)
''')

# Commit changes and close connection
conn.commit()
conn.close()
