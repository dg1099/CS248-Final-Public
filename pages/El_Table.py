import streamlit as st
from userAuth.user_profile import getName
import pandas as pd
import sqlite3
from datetime import datetime
from methodCalls import displayMenu
from methodCalls import displayMenu
from methodCalls import displayPreference
from streamlit_extras.stylable_container import stylable_container
from methodCalls import displayMenu
from methodCalls import displayPreference

# Setting the page size as defult wide( looks better :) )

#----------------------------CSS LAYOUT------------------------------------#\

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


st.markdown("""
    <style>
    .equal-height-container {
        display: flex;
        gap: 1rem;
        height: 100%;
    }
    .equal-height-box {
        flex: 1;
        background-color: #2E8B57;
        padding: calc(1em - 1px);
        border: 4px solid black;
        border-radius: 0.5rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    </style>
""", unsafe_allow_html=True)

######################
# ADDING TO FOOD LOG #
######################

def get_db_connection(db_path='food_tracker.db'):
    return sqlite3.connect(db_path)

def add_to_food_log(
    meal_id, uid, meal_type, food_name,
    calories, protein, fats, carbohydrates,
    db_path='food_tracker.db'
):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    date = datetime.now()  # or pass a custom date if needed
    
    query = '''
        INSERT INTO food_log (
            meal_id, date, uid, meal_type,
            food_name, calories, protein, fats, carbohydrates
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(query, (
        meal_id, date, uid, meal_type,
        food_name, calories, protein, fats, carbohydrates
    ))

    conn.commit()
    conn.close()

#----------------------------PAGE LAYOUT------------------------------------#


if "access_token" not in st.session_state:
    st.warning("Please first login!")
    #Stop from everything else from being loaded up if they have not loggedin 
else: 
    
    headCol1,headCol2=st.columns([8,2])

    #This is our header column so we can also have a popout section for prefrences
    with headCol1:
        st.subheader(f"Hello, {getName()[0]}",divider=True)
        st.write("Hours: Monday-Friday (9:00-3:00)")
        st.warning("Disclaimer: These nutritional facts are estimated using the Spoonacular API. Some may be incomplete or not entirely accurate.")
    with headCol2:
        displayPreference("eltable")

    displayMenu("cafehoop","coopMenus/el-table-dishes-filled.csv","coopMenus/el-table-drinks-filled.csv")

