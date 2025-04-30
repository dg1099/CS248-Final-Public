import streamlit as st
from userAuth.auth import google_login
from userAuth.user_profile import render_user_profile
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.app_logo import add_logo
from userAuth.user_profile import getName
from Database_files.add_userData import get_preference
import sqlite3
from datetime import datetime
import pandas as pd
import wellesley_fresh_api
#st.set_page_config(page_title="RYD To Eat", page_icon="https://drive.google.com/file/d/1wdFemFBErLC6bXpJ5jvKKp6q3a0tIRVt/view?usp=sharing")

############################################################################
##################### Private Database Configuration ########################
############################################################################
import os
import subprocess


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


############################################################################
##################### UPDATING AND GETTING allergens########################
############################################################################

def change_allergens(username, allergens):
    # Convert allergens list to comma-separated string
    pref_string = ",".join(allergens)

    # Connect to your database
    conn = sqlite3.connect(DB_PATH)  # change to your actual DB file
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

def get_user_allergens(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT allergens FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result and result[0]:
            return result[0].split(",")  # Returns list of allergens
        return []
    finally:
        conn.close()

##################### UPDATING AND GETTING CALORIE GOALS ########################

#-----------------------IMPORTANT METHODS FOR SITE-----------------------------#

#Fot google sign in 
DEBUG = False

def fake_login():
    """Sets a fake access token and user info for debugging."""
    st.session_state["access_token"] = "fake-token"
    st.session_state["fake_user_name"] = "Test Student"
    st.session_state["fake_user_picture"] = "https://i.pravatar.cc/60?img=25"  # random placeholder

def login_sidebar():
    st.sidebar.title("Welcome!")

    if DEBUG and "access_token" not in st.session_state:
        fake_login()

    # If already logged in
    if "access_token" in st.session_state:
        render_user_profile()

        if st.sidebar.button("Logout"):
            for key in ["access_token", "oauth_state"]:
                st.session_state.pop(key, None)
            st.rerun()

    else:
        
        st.sidebar.write("Please log in with your Google account:")
        logged_in = google_login()
        st.sidebar.warning("Not logged in.")
        if logged_in:
            st.rerun()


#----------------------------CSS LAYOUT------------------------------------#\

st.html(
    """
<style>
[data-testid="stSidebarContent"] {
    color: white;
    background-color: #622572;
    border-radius: 25px;
    border-color: black;
    border-style: solid;
    border-width: 7px;
    background-image: url("https://images.unsplash.com/photo-1686593686409-43456910d65c?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8cHVycGxlJTIwYmFja2dyb3VuZHxlbnwwfHwwfHx8MA%3D%3D");
}
</style>
"""
)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1686593686409-43456910d65c?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8cHVycGxlJTIwYmFja2dyb3VuZHxlbnwwfHwwfHx8MA%3D%3D");
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align: center; '>RDY To Eat</h1>",
             unsafe_allow_html=True)

#----------------------------PAGE LAYOUT------------------------------------#

#Cite logo 
left_co, cent_co,last_co = st.columns(3)
with cent_co:
   
    st.image("./assets/R.D.Y. to Eat.png")




#This will create the side bar
login_sidebar()

if "access_token" not in st.session_state:
    st.warning("Please first login!")
    st.stop() #Stop from everything else from being loaded up if they have not loggedin 

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

with st.expander("Welcome!"):
    with stylable_container(
                key=f"container_with_bordew2323e23e",
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
        st.markdown("""With RdyToEat, you can easily 
                log meals from Cafe Hoop, El Table, and 
                any Wellesley dining hall. In your personal
                    journal, you'll get daily, weekly, and monthly 
                breakdowns of your meals, helping you track the foods 
                you loved, and the ones that might need a little improvement.
                    You'll also find detailed nutrition graphs and can set personal 
                meal goals to stay on track. We’re excited to have you join us 
                on your food journey!""")

with stylable_container(
            key="container_with_border23",
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

    
    st.subheader("Whats Happening in the Halls right now!")
    st.warning("Please log your meals in the Wellesley Fresh Meals Tab")

    with st.expander("Take a sneek peek at your most frequented hall!"):
        st.write("hey")
    email=getName()[1]
    fav_hall=get_preference(email)
    if fav_hall!=None:
        options=["Lulu","Bates","Stone D","Tower"]
        default_fav=options.index(fav_hall)
        fav_option=st.selectbox("Select A Hall!",options,index=default_fav)
    else:
        options=["Lulu","Bates","Stone D","Tower"]
        fav_option=st.selectbox("Select A Hall!",options)
    
    date=datetime.now().date()
    timenow=datetime.now()
    current_hour=timenow.hour
    col12,=st.columns(1,vertical_alignment="center")

    with col12:
        if 5 <= current_hour < 10:
            selected_time="Breakfast"
            st.warning(f"For {selected_time} at {fav_option}")
            data = wellesley_fresh_api.wellesleyCall(
                            fav_option, 
                            selected_time, 
                            date)
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
            cleandf=cleandf.drop_duplicates(subset=["name"])

            cleandf= cleandf.loc[(cleandf["date"].str.split("T").str[0]==str(date))]
            for item in cleandf["name"].items():
                st.write(item[1])


        elif 10 <= current_hour < 14:
            selected_time="Lunch"
            st.warning(f"For {selected_time} at {fav_option}")

            data = wellesley_fresh_api.wellesleyCall(
                            fav_option, 
                            selected_time, 
                            date)
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
            cleandf=cleandf.drop_duplicates(subset=["name"])

            cleandf= cleandf.loc[(cleandf["date"].str.split("T").str[0]==str(date))]
            for item in cleandf["name"].items():
                st.write(item[1])
        elif 14 <= current_hour < 21:
            selected_time="Dinner"
            st.warning(f"For {selected_time} at {fav_option}")

            data = wellesley_fresh_api.wellesleyCall(
                            fav_option, 
                            selected_time, 
                            date)
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
            cleandf=cleandf.drop_duplicates(subset=["name"])

            cleandf= cleandf.loc[(cleandf["date"].str.split("T").str[0]==str(date))]
            for item in cleandf["name"].items():
                st.write(item[1])
        else:
            st.warning("All Dining Halls are closed!")

            
