import streamlit as st
import datetime
from datetime import date
from streamlit_extras.stylable_container import stylable_container
import wellesley_fresh_api
import pandas as pd
import sqlite3
from methodCalls import displayPreference
from Dashboard import DB_PATH
from userAuth.user_profile import getName
import wellesley_fresh_api 

# Setting the page size as defult wide( looks better :) )from userAuth.user_profile import getName


#----------------------------CSS LAYOUT------------------------------------#\

# This is to fix the sizing of our app logo
st.markdown(
    """
<style>
[data-testid="stSidebarContent"] {
    border-radius: 25px;
    border-style: solid;
    border-width: 7px;
    background-image: url("https://static.vecteezy.com/system/resources/previews/008/359/817/non_2x/beautiful-and-bright-yellow-and-purple-color-gradient-background-combination-soft-and-smooth-texture-free-vector.jpg");
}
</style>
""",
    unsafe_allow_html=True
)

# This is to make sure our app has a background image
st.markdown(
    """
    <style>
    .stApp {
        opacity: 100;
        background-image: url("https://static.vecteezy.com/system/resources/previews/008/359/817/non_2x/beautiful-and-bright-yellow-and-purple-color-gradient-background-combination-soft-and-smooth-texture-free-vector.jpg");
    }
    </style>
    """,
    unsafe_allow_html=True
)

# This is to make sure our boxes are the same height
st.markdown("""
    <style>
    .equal-height-container {
        display: flex;
        gap: 1rem;
        height: 100%;
    }
    .equal-height-box {
        flex: 1;
        background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
        padding: calc(1em - 1px);
        border: 4px solid black;
        border-radius: 0.5rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    </style>
""", unsafe_allow_html=True)


# This is to fix the sizing of our app logo 
st.markdown("""    
<style>            
img[data-testid="stLogo"] {
            height: 3.2rem;
}          
</style.
""",
unsafe_allow_html=True
)
st.logo("assets/R.D.Y. to Eat.png",icon_image="assets/R.D.Y. to Eat.png")
######################
# ADDING TO FOOD LOG #
######################

# This function adds a meal to the food log in the database
def add_to_food_log(meal_id, uid, meal_type, food_name, calories, protein, fats, carbohydrates, date, location,db_path=DB_PATH):
    try:
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

######################
# ADD A RATING TO DB #
######################
# This function inserts a rating into the database
def insert_rating(mealname, uid, rating, comment, emotion):

    # Insert into the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO rating (meal, uid, rating, comment, emotion)
            VALUES (?, ?, ?, ?, ?)
        """, (mealname, uid, rating, comment, emotion))

    conn.commit()
    conn.close()
    st.success("Rating submitted successfully!")

#----------------------------PAGE LAYOUT------------------------------------#

if "access_token" not in st.session_state:
    st.warning("Please first login! Click on our logo to the left to open the sidebar to login!")
    #Stop from everything else from being loaded up if they have not loggedin 
else: 
    
    # This is to set the page layout to wide so it looks better
    headCol1,headCol2=st.columns([8,2])

    #This is our header column so we can also have a popout section for prefrences
    with headCol1:
        st.subheader(f"Hello, {getName()[0]}",divider=True)
    with headCol2:
        currentpref=displayPreference("wellesleyfresh")

    # This is the expander that gives an overview of the page and what it does
    with st.expander("✨ Page Overview!"):
        st.write("""
        **Welcome to the Dining Hall Menu Generator!** 🍽️

        - 🕐 Pick your **Meal Time** (Breakfast, Lunch, Dinner)  
        - 🏠 Choose your **Dining Hall** (Lulu, Tower, Bates, Stone D)  
        - 📅 Select a **Date** to view the menu  
        - 📋 Hit **Generate!** to see meals that match your preferences  
        - ❌ Automatically filters out meals based on your dietary preferences  
        - ✅ Add selected meals to your personal food log
        """)
    
    # This is the columns that layout meal and dining hall options 
    col1,col2,col3=st.columns(3)

    # This is the container that will hold the meal time and dining hall options
    with col1:
        with stylable_container(
            key="container_with_border2313",
            css_styles="""
                {
                    border-radius: 0.5rem;
                    background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                    padding: calc(1em - 1px)
                         
                }
                """,
        ):
            st.subheader("Pick Meal Time!")
            
            
            # These are the buttons that will allow the user to select the meal time they want to see the menu for
            breakfast=st.button("Breakfast")
            lunch=st.button("Lunch")
            dinner=st.button('Dinner')

            #SO here we have a button that keeps track of the session state of the time the student selects 
            if breakfast:
                st.session_state["selected_time"] = "Breakfast"
            elif lunch:
                st.session_state["selected_time"] = "Lunch"
            elif dinner:
                st.session_state["selected_time"] = "Dinner"
            

            
    # This is the container that will hold the dining hall options
    with col2:
        with stylable_container(
            key="container_with_border1",
            css_styles="""
                {
                    border-radius: 0.5rem;
                    background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                    padding: calc(1em - 1px)
                      
                }
                """,
        ):
            
            st.subheader("Pick a Dining Hall!")
            
            # These are the buttons that will allow the user to select the dining hall they want to see the menu for
            lulu=st.button("Lulu")
            tower=st.button("Tower")
            bates=st.button("Bates")
            stone=st.button("Stone D")

            

            # This makes sure that we keep track in the session state dictionary what hall studnets are eating at 
            if lulu:
                st.session_state["selected_hall"] = "Lulu"
            elif tower:
                st.session_state["selected_hall"] = "Tower"
            elif bates:
                st.session_state["selected_hall"] = "Bates"
            elif stone:
                st.session_state["selected_hall"] = "Stone D"
            
            
            
    # This is the container that will generate the menu based on the meal time and dining hall selected by the user
    # and the date they selected.
    with col3:
        with stylable_container(
            key="container_with_border2",
            css_styles="""
                {
                    border-radius: 0.5rem;
                    background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                    padding: calc(1em - 1px)
                    
                    
                }
                """,
        ):
            st.subheader("Generate Menu!")

            #Makes it so the calander is already on the current date
            d = st.date_input("Meal Date", "today")
            
            st.session_state["date"] = d
            st.write("")
            generate=st.button("Generate!")

    #Makes the list that will hold all the meals picked by the user
    if "wellesleymeal" not in st.session_state:
        st.session_state["wellesleymeal"] = []


# This is the main logic of the app that will generate the menu based on the meal time and dining hall selected by the user
# and the date they selected.
    if generate:

        if "selected_hall" not in st.session_state or "selected_time" not in st.session_state:
            st.warning("You forgot to select a Meal Time or Dining Hall")
            st.stop()
        data = wellesley_fresh_api.wellesleyCall(
                st.session_state["selected_hall"], 
                st.session_state["selected_time"], 
                st.session_state["date"])
        df = pd.json_normalize(data)
        
        
        try:
            cleandf = df[['name', 
                        'nutritionals.calories',
                        'nutritionals.fat', 
                        'nutritionals.carbohydrates', 
                        'nutritionals.protein',
                        "description",
                        "allergens",
                        "date"]]
        except:
            cleandf = df[['name',
                        "description",
                        "allergens",
                        "date"]]
        

        cleandf= cleandf.loc[(cleandf["date"].str.split("T").str[0]==str(st.session_state["date"]))]
        cleandf=cleandf.drop_duplicates(subset=["name"])
        
        # This drop all the rows with items that dont have your prefreneces 
        drop_row=[]

        for index,item in cleandf["allergens"].items():
            for item1 in item:
                print(item1["name"])
                print(currentpref)
                if item1["name"] in currentpref:
                    drop_row.append(index)
        
        cleandf=cleandf.drop(drop_row)

        if cleandf.empty:
            st.warning("No meal options match your current preferences!")
            st.stop()


        st.session_state["dataframe"] = cleandf

        
        st.session_state["tempdataframe"] = cleandf

        
    if "dataframe" not in st.session_state:
        st.warning("Please generate a menu first!")
        st.stop()

    # So its better to take it out of the loop to get rid of the constant loops 
    con1=st.container()

    with con1:
        with stylable_container(
            key="container_with_border23",
            css_styles=["""
            
                {
                    border-radius: 0.5rem;
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
            st.subheader("Menu")

            #allows users to see what meal opetion they choose
            st.markdown(
                f"""
                <h2 style="
                    background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);

                    You chose {st.session_state['selected_hall']} for {st.session_state['selected_time']}
                </h2>
                """,
                unsafe_allow_html=True
            )


            
            # Search bar to filter meals by name
            search=st.text_input("Search for a Meal!")
            if search:
                # Filter the dataframe based on the search input
                st.session_state["dataframe"] = st.session_state["dataframe"][st.session_state["dataframe"]['name'].str.contains(search, case=False, na=False)]
                if st.session_state["dataframe"].empty:
                    st.warning("No meals found matching your search criteria.")
                    st.stop()
            else:
                st.session_state["dataframe"] = st.session_state["tempdataframe"]


            # Display the meal name and calorie count in a table format
            namecol,menucol,buttoncol=st.columns(3)
            with namecol:
                st.write("Meal Name")
            with menucol:
                st.write("Calorie Count")

            # This is the loop that will display all the meals in a table format
            for idx,(mealname,calories,description) in  enumerate(zip(st.session_state["dataframe"]['name'], st.session_state["dataframe"]['nutritionals.calories'],st.session_state["dataframe"]["description"])):
                col1,col2,col3=st.columns(3,border=True)
                
                with col1:
                    # This is the container that will hold the meal name and description
                    with stylable_container(
        key=f"table3{mealname}{calories}",
        css_styles="""
            {
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,
    ):
                        st.markdown(mealname, help=description)
                with col2:
                    st.write(calories)
                with col3:
                    session_key = f"{mealname}_{idx}_added"

                    # Button to add the meal
                    mealb = st.button("Add To Journal", key=session_key, use_container_width=True)

                    #Thsi will allow us to store the star raitng of the dishes 
                    if "starrating" not in st.session_state:
                        st.session_state["starrating"]=[]
                    
                    #Star rating popover in streamlit 
                    with st.popover("Rating",icon="👋"):
                        with st.form(key=f"{mealname}_{idx}_"):
                            # Emoji selection for feelings about the meal
                            emoji_labels = {
                                "😡": "Horrible",
                                "😕": "Okay",
                                "😐": "Neutral",
                                "🙂": "Happy",
                                "😍": "Love"
                            }

                            # Text input for meal comment
                            comment=st.text_input("Add your meal comment here!",key=f"{mealname}_")
                            st.write("How do you feel about this?")

                            selected_emoji = st.select_slider(
                                "How do you feel about this?",
                                options=["😡", "😕", "😐", "🙂", "😍"],
                                key=f"{mealname}_emoji"
                            )

                            # Show result
                            if selected_emoji:
                                emotion_label = emoji_labels[selected_emoji]
                                st.write(f"You selected: {selected_emoji}")

                            sentiment_mapping = ["1", "2", "3", "4", "5"]
                            selected = st.feedback("stars",key=session_key+"rating")

                            submitted = st.form_submit_button("Submit")# This is the submit button for the form

                            # Check if the form was submitted and a rating was selected
                            if submitted:
                                st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
                                insert_rating(mealname, getName()[1], sentiment_mapping[selected], comment, emotion_label)
                                
                                #This stores all the rating made into a session state 
                                if session_key not in st.session_state["starrating"]:
                                    st.session_state["starrating"].append(session_key+"_"+sentiment_mapping[selected]+"_"+comment+"_"+str(selected_emoji))
                                    rat = st.session_state["starrating"][len(st.session_state["starrating"])-1][-1]
                                    print(f"######## RATING: {rat} ########")

                                     

                    # Add to session state if not already added
                    if mealb and session_key not in st.session_state["wellesleymeal"]:
                        # Store in session state
                        st.session_state["wellesleymeal"].append(session_key)

                        # Pull meal data
                        uid = getName()[1]  # assuming getName() returns (name, uid)
                        meal_type = st.session_state["selected_time"]
                        food_name = mealname
                        date_selected = st.session_state["date"]
                        
                        try:
                            date_str = date_selected.strftime("%Y-%m-%d")
                        except:
                            date_str = str(date_selected)

                        # Get nutritional info (handle missing gracefully)
                        cal = calories if pd.notnull(calories) else 0
                        fat = st.session_state["dataframe"]['nutritionals.fat'].iloc[idx] if pd.notnull(st.session_state["dataframe"]['nutritionals.fat'].iloc[idx]) else 0
                        carbs = st.session_state["dataframe"]['nutritionals.carbohydrates'].iloc[idx] if pd.notnull(st.session_state["dataframe"]['nutritionals.carbohydrates'].iloc[idx]) else 0
                        protein = st.session_state["dataframe"]['nutritionals.protein'].iloc[idx] if pd.notnull(st.session_state["dataframe"]['nutritionals.protein'].iloc[idx]) else 0
                        location=st.session_state["selected_hall"]
                        # Use index as meal_id or something more unique if needed
                        meal_id = f"{date_str.replace('-', '')}{idx}"

                        # Call the new DB function
                        add_to_food_log(
                            meal_id=meal_id,
                            uid=uid,
                            meal_type=meal_type,
                            food_name=food_name,
                            calories=cal,
                            protein=protein,
                            fats=fat,
                            carbohydrates=carbs,
                            date=date_str,
                            location=location
                        )


                    # Show confirmation
                    if session_key in st.session_state["wellesleymeal"]:
                        st.warning("Added to Journal")
    















