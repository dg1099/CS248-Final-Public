import sqlite3
from datetime import datetime

##################### UPDATING AND GETTING allergens########################
def change_allergens(username, allergens):
    # Convert allergens list to comma-separated string
    pref_string = ",".join(allergens)

    # Connect to your database
    conn = sqlite3.connect("food_tracker.db")  # change to your actual DB file
    cursor = conn.cursor()

    try:
        # Update the user's allergens
        cursor.execute(
            "UPDATE user SET allergens = ? WHERE username = ?",
            (pref_string, username)
        )
        conn.commit()
        print("allergens updated successfully.")
    except sqlite3.Error as e:
        print("An error occurred:", e)
    finally:
        conn.close()

def get_allergens(username):
    conn = sqlite3.connect("food_tracker.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT allergens FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result and result[0]:
            return result[0].split(",")  # Returns list of allergens
        return []
    finally:
        conn.close()


######################
# ADDING TO FOOD LOG #
######################

def get_db_connection(db_path='food_tracker.db'):
    return sqlite3.connect(db_path)

def add_to_food_log(
    meal_id, uid, meal_type, food_name,
    calories, protein, fats, carbohydrates,location,
    db_path='food_tracker.db'
):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Optional: clean formatting

    query = '''
        INSERT INTO food_log (
            meal_id, date, uid, meal_type,
            food_name, calories, protein, fats, carbohydrates,location_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    '''
    cursor.execute(query, (
        meal_id, date, uid, meal_type,
        food_name, calories, protein, fats, carbohydrates
    ))

    conn.commit()
    conn.close()


#This will update the prefrences 
def update_preference(username, new_preference):
    conn = sqlite3.connect("food_tracker.db")
    cursor = conn.cursor()

    # Update the preferences field with the new preference for the specified user
    cursor.execute("""
    UPDATE user 
    SET preferences = ? 
    WHERE username = ?
    """, (new_preference, username))

    conn.commit()
    conn.close()

    print(f"Preference updated for user {username} to: {new_preference}")

#Get the prefrences of the user for their favorite halls 
def get_preference(username):
    conn = sqlite3.connect("food_tracker.db")
    cursor = conn.cursor()

    # Query to fetch the preferences for the specified user
    cursor.execute("""
    SELECT preferences 
    FROM user 
    WHERE username = ?
    """, (username,))
    
    # Fetch the result
    result = cursor.fetchone()

    conn.close()

    # If the user is found and has preferences set, return it
    if result:
        return result[0]
    else:
        return None  # Return None if no preferences are found