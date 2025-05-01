import streamlit as st
from userAuth.user_profile import getName
import pandas as pd
from methodCalls import displayMenu
from methodCalls import displayPreference

#----------------------------CSS LAYOUT------------------------------------#\
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
#----------------------------PAGE LAYOUT------------------------------------#

# Hours for cafe hoop and el table


if "access_token" not in st.session_state:
    st.warning("Please first login! Click on our logo to the left to open the sidebar to login!")
    #Stop from everything else from being loaded up if they have not loggedin 
else: 
    
    headCol1,headCol2=st.columns([8,2])

    #This is our header column so we can also have a popout section for prefrences
    with headCol1:
        st.subheader(f"Hello, {getName()[0]}",divider=True)
        st.write("Hours: Wed-Thurs from 9pm-12am, Fri-Sat from 10pm-1am")
        st.warning("Disclaimer: These nutritional facts are estimated using the Spoonacular API. Some may be incomplete or not entirely accurate.")
        with st.expander("✨ Page Overview!"):
            st.write("""
            **Welcome to the Dining Hall Menu Viewer!** 🥗

            - 🧑‍🍳 View the **full meal offerings** from El Table based on your preferences  
            - 📊 See **nutritional info** like calories, protein, fats, and carbs for each meal  
            - ✅ Use the **checkboxes** to add meals to your personal **Food Log**  
            - 📆 Meals are updated **daily**, based on the latest CSV data  
            - ⚠️ Nutritional data is fetched via Spoonacular API and may be incomplete or estimated  
            - 🧠 Your preferences help filter items for **a personalized experience**
            """)
    with headCol2:
        displayPreference("cafehoop")
            
    displayMenu("cafehoop","coopMenus/cafe-hoop-dishes-filled.csv","coopMenus/cafe-hoop-drinks-filled.csv")
