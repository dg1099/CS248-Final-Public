import streamlit as st
from userAuth.user_profile import getName
import pandas as pd
from methodCalls import displayMenu
from methodCalls import displayPreference

#----------------------------CSS LAYOUT------------------------------------#\

st.markdown(
    """
<style>
[data-testid="stSidebarContent"] {
    color: white;
    background-color: #622572;
    border-radius: 25px;
    border-color: black;
    border-style: solid;
    border-width: 7px;
    background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20210421/pngtree-cream-purple-vintage-paper-texture-premium-quality-background-image_636174.jpg");
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
        background-image: url("https://img.freepik.com/premium-vector/hand-painted-watercolor-blue-abstract-background_278222-7243.jpg?semt=ais_hybrid&w=740");
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
    st.warning("Please first login!")
    #Stop from everything else from being loaded up if they have not loggedin 
else: 
    
    headCol1,headCol2=st.columns([8,2])

    #This is our header column so we can also have a popout section for prefrences
    with headCol1:
        st.subheader(f"Hello, {getName()[0]}",divider=True)
        st.write("Hours: Wed-Thurs from 9pm-12am, Fri-Sat from 10pm-1am")
        st.warning("Disclaimer: These nutritional facts are estimated using the Spoonacular API. Some may be incomplete or not entirely accurate.")
    with headCol2:
        displayPreference("cafehoop")
            
    displayMenu("cafehoop","coopMenus/cafe-hoop-dishes-filled.csv","coopMenus/cafe-hoop-drinks-filled.csv")
