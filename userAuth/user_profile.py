import streamlit as st
import sqlite3
import requests
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

@st.cache_data(ttl=3600)
def get_user_info(access_token):
    """Fetch and cache user profile info from Google."""
    try:
        response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.warning(f"User info fetch failed: {e}")
    return None


# This is how show user profile 
def render_user_profile():
    """Render user profile photo and greeting, if user opts in."""
    access_token = st.session_state.get("access_token") #User access token here 
    if not access_token:
        return


    #Dont need this feature right nwo 
    #show_profile = st.sidebar.checkbox("Show profile info", value=True) 

    #This will display the users google profile picture 
    if "fake_user_name" in st.session_state:
        first_name = st.session_state["fake_user_name"]
        picture = st.session_state["fake_user_picture"]
    else:
        user = get_user_info(access_token)
        if not user:
            st.sidebar.success("Logged in ✅")
            return
        email = user.get("email")
        first_name = user.get("given_name") or user.get("name", "there").split()[0]
        picture = user.get("picture")

        #create user or access user data if it already exists
        st.session_state["uid"] = create_user(email)
        # Had to make this look better 
        col1, col2 = st.sidebar.columns([3, 14])
        with col1:
            st.image(picture, width=60)
        with col2:
            st.markdown(f"**Hello, {first_name}!**")

    
def create_user(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the user already exists
    cursor.execute("SELECT uid FROM user WHERE username = ?", (email,))
    result = cursor.fetchone()
    
    if not result:
        # Insert user
        cursor.execute("INSERT INTO user (username) VALUES (?);", (email,))
        conn.commit()

    conn.close()

    return result

def getName():
    """Render user profile photo and greeting, if user opts in."""
    access_token = st.session_state.get("access_token") #User access token here 
    if not access_token:
        return


    #Dont need this feature right nwo 
    #show_profile = st.sidebar.checkbox("Show profile info", value=True) 

    #This will display the users google profile picture 
    if "fake_user_name" in st.session_state:
        first_name = st.session_state["fake_user_name"]
    else:
        user = get_user_info(access_token)
        email = user.get("email")
        first_name = user.get("given_name") or user.get("name", "there").split()[0]
    return (first_name,email) 
