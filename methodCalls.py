import streamlit as st
import pandas as pd
from userAuth.user_profile import getName
from Dashboard import change_allergens
from Dashboard import get_user_allergens
from streamlit_extras.stylable_container import stylable_container


def displayMenu(location,file1,file2):
    tab1,tab2=st.tabs(["Meals","Drinks"])

    df = pd.read_csv(file1)
    with tab1:
        with stylable_container(
            key=f"container_with_border12{location}",
            css_styles=["""
            
                {
                    
                    border: 4px solid black;
                    border-radius: 0.5rem;
                    background: #b89927;
                    background: linear-gradient(90deg,rgba(184, 153, 39, 1) 0%, rgba(113, 20, 163, 1) 91%);
                    background-color: #2E8B57;
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
            if f"meals{location}" not in st.session_state:
                st.session_state[f"meals{location}"] = []

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

            for idx,(meal,ingr) in  enumerate(zip(df["Meal Name"], df["Calories"])):
                col1,col2,col3=st.columns(3,border=True)
                
                
                with col1:
                    st.write(meal)
                with col2:
                    st.write(ingr)
                with col3:
                    session_key = f"{meal}_{idx}_added"

                    drinkb=st.button("Add To Journal", key=session_key,use_container_width=True)
                    
                    # Save button press result into the session dict
                    

                    if drinkb:
                        st.session_state[f"meals{location}"].append(session_key)
                    if session_key in st.session_state[f"meals{location}"]:
                        st.warning("Added to Journal")
            st.write(st.session_state[f"meals{location}"])

    with tab2: 
        with stylable_container(
            key=f"container_with_bordew2ewqw{location}",
            css_styles=["""
            
                {
                    border: 4px solid black;
                    border-radius: 0.5rem;
                    background: #b89927;
                    background: linear-gradient(90deg,rgba(184, 153, 39, 1) 0%, rgba(113, 20, 163, 1) 91%);
                    background-color: #2E8B57;
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

            cols1,cols2,cols3=st.columns(3)
            with cols1:
                st.write("Meal Name")
            with cols2:
                st.write("Calorie Count")

            for ind, (drink, cals) in enumerate(zip(df["Drink Name"], df["Calories"])):
                

                col1,col2,col3=st.columns(3,border=True)
                with col1:
                    st.write(drink)
                with col2:
                    st.write(cals)
                with col3:
                    session_key1 = f"{drink}_{ind}_added"

                    drinkb=st.button("Add To Journal", key=session_key1,use_container_width=True)
                    
                    # Save button press result into the session dict
                    

                    if drinkb:
                        st.session_state[f"drink{location}"].append(session_key1)
                    if session_key1 in st.session_state[f"drink{location}"]:
                        st.warning("Added to Journal")
                
                
                
                                
        st.write(st.session_state[f"meals{location}"])
        st.write(st.session_state[f"drink{location}"])

def displayPreference(location):
    
    with st.popover("Preferences",use_container_width=True):
        with stylable_container(
            key=f"container_with_border{location}",
            css_styles="""
                {
                    border: 4px solid black;
                    background: #b89927;
                    background: linear-gradient(90deg,rgba(184, 153, 39, 1) 0%, rgba(113, 20, 163, 1) 91%);
                    background-color: #2E8B57;
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


