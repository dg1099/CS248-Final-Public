import streamlit as st
import pandas as pd
from userAuth.user_profile import getName
from Dashboard import change_allergens
from Dashboard import get_user_allergens
from streamlit_extras.stylable_container import stylable_container
import sqlite3
from Dashboard import DB_PATH
import datetime
from datetime import datetime

# This function displays the menu for meals and drinks
def displayMenu(location,file1,file2):
    def add_to_food_log(meal_id, uid, meal_type, food_name, calories, protein, fats, carbohydrates, date, location,db_path= DB_PATH):
        try:
            # Connect to the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO food_log (
                    meal_id, date, uid, meal_type,
                    food_name, calories, protein, fats, carbohydrates,location_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                meal_id, date, uid, meal_type,
                food_name, calories, protein, fats, carbohydrates,location
            ))

            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"An error occurred while saving to the journal: {e}")
    
    tab1,tab2=st.tabs(["Meals","Drinks"])
    ## Load the CSV files for meals and drinks
    df = pd.read_csv(file1)
    with tab1:
        with stylable_container(
            key=f"container_with_border12{location}",
            css_styles=["""
            
                {
                    
                    border-radius: 0.5rem;
                    background: #b89927;
                    background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                    padding: calc(1em - 1px)
                        
                         
                }
                """,
                """
                div[data-testid="stMarkdownContainer"] p {
                    font-family: 'Lexend', sans-serif;
                    font-size: 1.1rem;
                    font-weight: 500;

                }
                """],
                

                
        ):
            # Check if the session state for meals exists, if not, initialize it
            if f"meals{location}" not in st.session_state:
                st.session_state[f"meals{location}"] = []

            # Display the meals dataframe
            search=st.text_input("Search for a Meal!",key=f"{location}meal")
            if search:
                # Filter the dataframe based on the search input
                df = df[df['Meal Name'].str.contains(search, case=False, na=False)]
                if df.empty:
                    st.warning("No meals found matching your search criteria.")
                    st.stop()
            else:
                df = df
            cols1,cols2,cols3=st.columns(3)
            with cols1:
                st.write("Meal Name")
            with cols2:
                st.write("Calorie Count")

            # Iterate through the dataframe and display each meal with its calorie count
            for idx,(meal,ingr) in  enumerate(zip(df["Meal Name"], df["Calories"])):
                col1,col2,col3=st.columns(3,border=True)
                
                
                with col1:
                    st.write(meal)
                with col2:
                    if ingr != "No Info":
                        cals = str(round(float(ingr), 2))
                        st.write(cals)
                    else:
                        st.write(ingr)
                with col3:
                    session_key = f"{meal}_{idx}_added"

                    drinkb=st.button("Add To Journal", key=session_key,use_container_width=True)
                    
                    #date
                    import datetime
                    current_date = datetime.date.today()
                    date = current_date.strftime("%Y-%m-%d")
                    meal_id = f"{date.replace('-', '')}{idx}"
                    # Save button press result into the session dict
                    if drinkb:
                        st.session_state[f"meals{location}"].append(session_key)
                        meal_name = df["Meal Name"].iloc[idx] if pd.notnull(df["Meal Name"].iloc[idx]) else "Unknown"
                        calories = df["Calories"].iloc[idx] if pd.notnull(df["Calories"].iloc[idx]) else 0
                        protein = df["Protein"].iloc[idx] if pd.notnull(df["Protein"].iloc[idx]) else 0
                        fat = df["Fat"].iloc[idx] if pd.notnull(df["Fat"].iloc[idx]) else 0
                        carbs = df["Carbohydrates"].iloc[idx] if pd.notnull(df["Carbohydrates"].iloc[idx]) else 0
                        from datetime import datetime
                        current_hour = datetime.now().hour
                        
                        # Determine meal type based on the current hour
                        if 5 <= current_hour < 11:
                            meal_type = "Breakfast"
                        elif 11 <= current_hour < 15:
                            meal_type = "Lunch"
                        elif 15 <= current_hour < 24:
                            meal_type = "Dinner"
                        else:
                            meal_type = "Snack"

                        # Add the meal to the food log
                        add_to_food_log(
                            meal_id,
                            getName()[1],
                            meal_type,
                            meal_name,
                            calories,
                            protein,
                            fat,
                            carbs,
                            date,
                            location,
                            db_path=DB_PATH
                        )
                    # Check if the meal has already been added to the journal
                    if session_key in st.session_state[f"meals{location}"]:
                        st.warning("Added to Journal")
            
    # Display the drinks tab
    with tab2: 
        with stylable_container(
            key=f"container_with_bordew2ewqw{location}",
            css_styles=["""
            
                {
                    border-radius: 0.5rem;
                    background: #b89927;
                    background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                    padding: calc(1em - 1px)
                         
                }
                """,
                """
                div[data-testid="stMarkdownContainer"] p {
                    font-family: 'Lexend', sans-serif;
                    font-size: 1.1rem;
                    font-weight: 500;
                }
                """],

                
        ):
            # Check if the session state for drinks exists, if not, initialize it
            if f"drink{location}" not in st.session_state:
                st.session_state[f"drink{location}"] = []

            df = pd.read_csv(file2)

            search=st.text_input("Search for a Meal!", key=f"{location}drink")
            if search:
                # Filter the dataframe based on the search input
                df = df[df['Drink Name'].str.contains(search, case=False, na=False)]
                if df.empty:
                    st.warning("No meals found matching your search criteria.")
                    st.stop()
            else:
                df = df

            # Display the drinks dataframe
            cols1,cols2,cols3=st.columns(3)
            with cols1:
                st.write("Meal Name")
            with cols2:
                st.write("Calorie Count")

            # Iterate through the dataframe and display each drink with its calorie count
            for ind, (drink, cals) in enumerate(zip(df["Drink Name"], df["Calories"])):
                
                # Create columns for drink name, calorie count, and button
                col1,col2,col3=st.columns(3,border=True)
                with col1:
                    st.write(drink)
                with col2:
                    st.write(cals)
                with col3:
                    session_key1 = f"{drink}_{ind}_added"

                    drinkb=st.button("Add To Journal", key=session_key1,use_container_width=True)
                    #date
                    import datetime
                    current_date = datetime.date.today()
                    date = current_date.strftime("%Y-%m-%d")
                    meal_id = f"{date.replace('-', '')}{ind}"
                    # Save button press result into the session dict

                    from datetime import datetime
                    current_hour = datetime.now().hour


                    # Check if the button was pressed
                    if drinkb:
                        st.session_state[f"drink{location}"].append(session_key1)
                        meal_name = df["Drink Name"].iloc[ind] if pd.notnull(df["Drink Name"].iloc[ind]) else "Unknown"
                        calories = df["Calories"].iloc[ind] if pd.notnull(df["Calories"].iloc[ind]) else 0
                        protein = df["Protein"].iloc[ind] if pd.notnull(df["Protein"].iloc[ind]) else 0
                        fat = df["Fat"].iloc[ind] if pd.notnull(df["Fat"].iloc[ind]) else 0
                        carbs = df["Carbohydrates"].iloc[ind] if pd.notnull(df["Carbohydrates"].iloc[ind]) else 0
                        
                        # Determine meal type based on the current hour
                        if 5 <= current_hour < 11:
                            meal_type = "Breakfast"
                        elif 11 <= current_hour < 15:
                            meal_type = "Lunch"
                        elif 15 <= current_hour < 24:
                            meal_type = "Dinner"
                        else:
                            meal_type = "Snack"

                        
                        # Add the drink to the food log
                        add_to_food_log(
                            meal_id,
                            getName()[1],
                            meal_type,
                            meal_name,
                            calories,
                            protein,
                            fat,
                            carbs,
                            date,
                            location,
                            db_path=DB_PATH
                        )
                    # Check if the drink has already been added to the journal
                    if session_key1 in st.session_state[f"drink{location}"]:
                        st.warning("Added to Journal")
                
# This function displays the user's dietary preferences in a popover
def displayPreference(location):
    
    with st.popover("Preferences",use_container_width=True):
        with stylable_container(
            key=f"container_with_border{location}",
            css_styles="""
                {
                    background: #b89927;
                    background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                    padding: calc(1em - 1px)
                         
                }
                """,
        ):
    # Get user email
            user_email = getName()[1]
            current_prefs = get_user_allergens(user_email)

            if "username" not in st.session_state:
                st.session_state["username"]=current_prefs
                

            # Define possible allergens
            all_possible_prefs = [
                "Peanuts", "Egg", "Fish", "Dairy", "Sesame", "Soy", "Tree Nut",
                "Wheat", "Shellfish", "Gluten Sensitive", "Vegan", "Vegetarian"
            ]

            # generate checkboxes dynamically
            selected_prefs = []
            for pref in all_possible_prefs:
                checked = pref in current_prefs
                if st.checkbox(pref, value=checked,key=f"{pref}{location}"):
                    selected_prefs.append(pref)

            # Save button
            if st.button("Save allergens"):
                change_allergens(user_email, selected_prefs)
                st.success("Your allergens have been updated!")
                st.rerun()  # force rerun to reflect changes immediately
            return current_prefs


