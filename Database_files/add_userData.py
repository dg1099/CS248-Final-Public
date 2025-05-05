import sqlite3
from datetime import datetime
import os
import subprocess
import streamlit as st

# from userAuth.user_profile import getName
def clone_private_repo():
    token = st.secrets["github"]["GITHUB_TOKEN"]
    repo_url = st.secrets["github"]["PRIVATE_DB_REPO"]
    db_file_name = st.secrets.get("DB_FILE_NAME", "food_tracker.db")

    if not token or not repo_url:
        raise ValueError("Missing GITHUB_TOKEN or PRIVATE_DB_REPO in secrets!")

    # Correct: clone into a folder
    clone_dir = "/tmp/private_repo"

    if not os.path.exists(clone_dir):
        subprocess.run(["git", "clone", repo_url.replace("https://", f"https://{token}@"), clone_dir], check=True)

    return os.path.join(clone_dir, db_file_name)

# Call this once in your app
DB_PATH = clone_private_repo()

##################### UPDATING AND GETTING allergens########################

# This function updates the user's allergens in the database
def change_allergens(username, allergens):
    # Convert allergens list to comma-separated string
    pref_string = ",".join(allergens)

    # Connect to your database
    conn = sqlite3.connect(DB_PATH )  # change to your actual DB file
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

# This function retrieves the user's allergens from the database
def get_allergens(username):
    conn = sqlite3.connect(DB_PATH )
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

# This function retrieves the user's name from the database
def get_db_connection(DB_PATH ):
    return sqlite3.connect(DB_PATH)


# This function adds a food item to the user's food log
def add_to_food_log(
    meal_id, uid, meal_type, food_name,
    calories, protein, fats, carbohydrates,location,
    db_path=DB_PATH 
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
    conn = sqlite3.connect(DB_PATH )
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
    conn = sqlite3.connect(DB_PATH )
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