import requests
import sqlite3
import csv
import streamlit as st

API_KEY = st.secrets('spooncular')

def apiCall(ingredient):
    url = f"https://api.spoonacular.com/recipes/parseIngredients"
    payload = {"ingredientList": ingredient, 'servings': 1, 'includeNutrition': True}
    response = requests.post(url, params={'apiKey': API_KEY}, data=payload)
    data = response.json()
    print(data)

    item_dict = {
                'Calories':'No Info',
                'Fat':'No Info',
                'Protein':'No Info',
                'Carbohydrates':'No Info'
                }
    
    if 'nutrition' in data[0]:
        nutrients = data[0]['nutrition']['nutrients']
        for n in nutrients:
            if n['name'] in item_dict.keys():
                item_dict[n['name']] = n['amount']
        return item_dict
    else:
        return item_dict

# Database connection
conn = sqlite3.connect("food_tracker.db")
c = conn.cursor()

# Ensure tables exist
c.execute('''
CREATE TABLE IF NOT EXISTS cafe_hoop (
    name TEXT PRIMARY KEY,
    calories REAL,
    fat REAL,
    protein REAL,
    carbohydrates REAL,
    ingredients_text TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS el_table (
    name TEXT PRIMARY KEY,
    calories REAL,
    fat REAL,
    protein REAL,
    carbohydrates REAL,
    ingredients_text TEXT
)
''')

conn.commit()

# Function to insert into correct table
def insert_from_csv(filename):
    if 'cafe-hoop' in filename.lower():
        table_name = 'cafe_hoop'
    elif 'el-table' in filename.lower():
        table_name = 'el_table'
    else:
        print(f"Skipping unknown file: {filename}")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        name_field = reader.fieldnames[0]  # Get item column name

        for row in reader:
            name = row[name_field].strip().lower()
            calories = float(row['Calories']) if row['Calories'] != 'No Info' else 0
            fat = float(row['Fat']) if row['Fat'] != 'No Info' else 0
            protein = float(row['Protein']) if row['Protein'] != 'No Info' else 0
            carbs = float(row['Carbohydrates']) if row['Carbohydrates'] != 'No Info' else 0
            ingredients = row['Ingredients']

            c.execute(f'''
                INSERT OR REPLACE INTO {table_name} (name, calories, fat, protein, carbohydrates, ingredients_text)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, calories, fat, protein, carbs, ingredients))
    
    conn.commit()
    print(f"Inserted data from: {filename}")

# List of filled CSVs (make sure these have nutritional data already)
filled_files = [
    "coopMenus/el-table-drinks-filled.csv",
    "coopMenus/el-table-dishes-filled.csv",
    "coopMenus/cafe-hoop-drinks-filled.csv",
    "coopMenus/cafe-hoop-dishes-filled.csv"
]

for file in filled_files:
    insert_from_csv(file)

c.close()
