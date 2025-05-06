# Author: Dianna Gonzalez
# Version: 5/6/25

# This code used the Spoonacular API to estimate nutrition facts for
# the Cafe Hoop and El Table menus. It created a database of all the
# ingredients and foods to avoid repetitive API calls

# Afterwards, the completed menus were added to the main database

import requests
import sqlite3
import csv
import streamlit as st
import time

## START OF API CODE ##

# this code only needed to be used once, api key will not work in this case
API_KEY = st.secrets('spooncular')

def apiCall(ingredient):
    """
    Call the Spoonacular API, specifically parseIngredients and collects only
    information about calories, fat, protein, and carbs
    """
    url = f"https://api.spoonacular.com/recipes/parseIngredients"
    payload = {"ingredientList": ingredient, 'servings': 1, 'includeNutrition': True}
    response = requests.post(url, params={'apiKey': API_KEY}, data=payload) # this url uses post instead of get
    data = response.json()
    print(data)

    # initializes all ingredients to 'No Info'
    item_dict = {
                'Calories':'No Info',
                'Fat':'No Info',
                'Protein':'No Info',
                'Carbohydrates':'No Info'
                }
    
    # if nutrition was in the data, it had all the information
    if 'nutrition' in data[0]:
        nutrients = data[0]['nutrition']['nutrients']
        for n in nutrients:
            if n['name'] in item_dict.keys():
                item_dict[n['name']] = n['amount']
        return item_dict
    else:
        return item_dict
    
def cache_ingredient(name, dct):
    """
    Inserts a new item into the database. The new item will have its information
    in a dictionary, which is taken in as a parameter
    """
    c.execute('''
        INSERT OR REPLACE INTO ingredients (name, calories, fat, protein, carbohydrates, ingredients_text)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, *dct.values()))
    conn.commit()
 
def get_cached_ingredient(name):
    """
    Gets the information of the food in the parameter from the database 
    and returns a dictionary of the data
    """
    c.execute('SELECT * FROM ingredients WHERE name = ?', (name,))
    row = c.fetchone()
    if row:
        return {
            'Calories': row[1],
            'Fat': row[2],
            'Protein': row[3],
            'Carbohydrates': row[4],
            'Ingredients': row[5]
         }
    return None

def fillMenu(filename):
    """
    This function looked at CSVs of the coop menus, filling in all the necessary data
    The menus either had only the name of the item or the name and its ingredients
    """
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        item_type = list(reader[0].keys())[0] # either drink  or meal
 
    with open(filename.replace('.csv', '-filled.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[item_type, 'Calories', 'Fat', 'Protein', 'Carbohydrates', 'Ingredients'])
        writer.writeheader()
 
        for row in reader:
            item = row[item_type].lower().strip()

            # enter if-else statements depending on how much information there is
            if row['Ingredients'] == '': # no ingredients, only name
                cached = get_cached_ingredient(item) # see if food is already in database
                if not cached:
                    print(f'{item} not in database, calling API')
                    cached = apiCall(item)
                    print(cached)
                    cached['Ingredients'] = 'No Info'
                    print(cached)
                    cache_ingredient(item, cached)
                row.update(cached)
 
            else: # has ingredients
                ing_list = [i.strip().lower() for i in row['Ingredients'].split(',')]
                cals = fats = protein = carbs = 0
 
                for ing in ing_list: # sum all ingredient information
                    cached = get_cached_ingredient(ing)
                    if not cached:
                        print(f'{item} not in database, calling API')
                        cached = apiCall(ing)
                        cached['Ingredients'] = ing
                        cache_ingredient(ing, cached)
 
                    if cached['Calories'] == 'No Info':
                        cals += 0
                        fats += 0
                        protein += 0
                        carbs += 0
                    else:
                        cals += cached['Calories']
                        fats += cached['Fat']
                        protein += cached['Protein']
                        carbs += cached['Carbohydrates']
 
                food_info = {
                            'Calories': cals,
                            'Fat': fats,
                            'Protein': protein,
                            'Carbohydrates': carbs,
                            'Ingredients': row['Ingredients']
                            }
                cache_ingredient(item, food_info)
                row.update(food_info)
 
            print(row)
            writer.writerow(row)
            print(f"Processed: {item}")
            time.sleep(2) # sleep to not overwhelm API
 
files = [
        "App Version 1\Menus Csv's\el-table-drinks.csv",
        "App Version 1\Menus Csv's\el-table-dishes.csv",
        "App Version 1/Menus Csv's/cafe-hoop-drinks.csv",
        "App Version 1/Menus Csv's/cafe-hoop-dishes.csv"
        ]
 
# code will not be able to connect
conn = sqlite3.connect("App Version 1/Menus Csv's/coop.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS ingredients (
    name TEXT PRIMARY KEY,
    calories REAL,
    fat REAL,
    protein REAL,
    carbohydrates REAL,
    ingredients_text TEXT
 )
''')
 
conn.commit()

# iterate through all menus
for file in files:
    fillMenu(file)
 
c.close()

## END OF API CODE ##

# This code adds the collected information from above into the main database
# Database connection
conn = sqlite3.connect("food_tracker.db") # outdated
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
