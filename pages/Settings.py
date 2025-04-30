import streamlit as st
from userAuth.auth import google_login
from userAuth.user_profile import render_user_profile
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.app_logo import add_logo
from userAuth.user_profile import getName
import sqlite3
from Database_files.add_userData import update_preference

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
    background-image: url("https://static.vecteezy.com/system/resources/previews/008/359/817/non_2x/beautiful-and-bright-yellow-and-purple-color-gradient-background-combination-soft-and-smooth-texture-free-vector.jpg");
}
</style>
"""
)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/008/359/817/non_2x/beautiful-and-bright-yellow-and-purple-color-gradient-background-combination-soft-and-smooth-texture-free-vector.jpg");
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.subheader("Settings",divider=True)

#----------------------------PAGE LAYOUT------------------------------------#





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




with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 4px solid black;
                border-radius: 0.5rem;
                background: #b89927;
                background: linear-gradient(90deg,rgba(184, 153, 39, 1) 0%, rgba(113, 20, 163, 1) 91%);
                background-color: #2E8B57;
                padding: calc(1em - 1px)
                        
            }
            """,
    ):
    st.subheader("Settings")
    username=st.text_input("Enter Your chosen username!")

    # Get user email
    user_email = getName()[1]
    current_prefs = get_user_allergens(user_email)


    #Added meal goal to profile
    st.subheader("Select Your Favorite Hall")
    lulu=st.button("Lulu")
    bates=st.button("Bates")
    stoned=st.button("Stone D")
    tower=st.button("Tower")

    st.session_state["fav_hall"]=""
    if lulu:
        st.session_state["fav_hall"]="Lulu"
    elif bates:
        st.session_state["fav_hall"]="Bates"
    elif stoned:
        st.session_state["fav_hall"]="Stone D"
    elif tower:
        st.session_state["fav_hall"]="Tower"
    
    if st.session_state["fav_hall"]!="":
        st.warning(f"Your favorite hall is {st.session_state["fav_hall"]}")

    update_preference(username=user_email,new_preference=st.session_state["fav_hall"])
    st.subheader("Allergen Settings")

    

    # Define possible allergens
    all_possible_prefs = [
        "Peanuts", "Egg", "Fish", "Dairy", "Sesame", "Soy", "Tree Nut",
        "Wheat", "Shellfish", "Gluten Sensitive", "Vegan", "Vegetarian"
    ]

    # generate checkboxes dynamically
    selected_prefs = []
    for pref in all_possible_prefs:
        checked = pref in current_prefs
        if st.checkbox(pref, value=checked):
            selected_prefs.append(pref)

    # Save button
    if st.button("Save Settings"):
        change_allergens(user_email, selected_prefs)
        st.success("Your allergens have been updated!")
        st.rerun()  # force rerun to reflect changes immediately
