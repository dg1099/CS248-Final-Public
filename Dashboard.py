import streamlit as st
from userAuth.auth import google_login
from userAuth.user_profile import render_user_profile
from streamlit_extras.stylable_container import stylable_container
from userAuth.user_profile import getName
import sqlite3
from datetime import datetime
import pandas as pd
import wellesley_fresh_api
import plotly.express as px
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import pytz


############################################### Datavisualization Functions #######################################################
# Function to visualize the most common dining hall visits 
def common_dining(uid):
    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()
    c.execute("SELECT location_id FROM food_log WHERE uid = ?", (uid, ))

    rows = c.fetchall()

    df = pd.DataFrame(rows, columns=["Dining Hall"])
    counts = df["Dining Hall"].value_counts().reset_index()
    counts.columns = ["Dining Hall", "# of Visits"]

    # 3. Sort in descending order
    counts = counts.sort_values("# of Visits", ascending=False)

    # 4. Plot horizontal bar chart
    fig = px.bar(
        counts,
        x="# of Visits",
        y="Dining Hall",
        orientation='h',  # horizontal
        color_discrete_sequence=["lightpink"]
    )

    fig.update_layout(yaxis=dict(categoryorder='total ascending'))  # most common at top
    
    return fig


############################################################################
##################### Private Database Configuration ########################
############################################################################
import os
import subprocess

# This function clones a private GitHub repository containing the database file
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
############################################################################
##################### UPDATING AND GETTING allergens########################
############################################################################

# This function updates the user's allergens in the database
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

# This function retrieves the user's allergens from the database
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

##################### SHOWING TOP 5 MEALS ########################
# This function retrieves the top-rated meals from the database
def topRated():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = '''
        SELECT meal, AVG(rating) as avg_rating
        FROM rating
        GROUP BY meal
        HAVING AVG(rating) > 4
        LIMIT 5
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#-----------------------IMPORTANT METHODS FOR SITE-----------------------------#

#Fot google sign in 
DEBUG = False

# This function sets a fake access token and user info for debugging purposes
def fake_login():
    """Sets a fake access token and user info for debugging."""
    st.session_state["access_token"] = "fake-token"
    st.session_state["fake_user_name"] = "Test Student"
    st.session_state["fake_user_picture"] = "https://i.pravatar.cc/60?img=25"  # random placeholder

#This is the login side bar that allows users to log into the site
def login_sidebar():
    st.sidebar.title("Welcome!")

    if DEBUG and "access_token" not in st.session_state:
        fake_login()

    # If already logged in
    if "access_token" in st.session_state:
        render_user_profile()

        #Mark down to make the button text black so its easier for users to view 
        st.markdown("""
            <style>
                div.stButton > button {
                    color: black !important;
                }
                </style>
            """, unsafe_allow_html=True)
        if st.sidebar.button("Logout"):
            for key in ["access_token", "oauth_state"]:
                st.session_state.pop(key, None)
            st.rerun()

    else:
        #Makes it so if the user has not logged in it will display a warning 
        st.sidebar.write("Please log in with your Google account:")
        logged_in = google_login()
        st.sidebar.warning("Not logged in.")
        if logged_in:
            st.rerun()


#----------------------------CSS LAYOUT------------------------------------#\

# This is to style the sidebar and main app background
st.html(
    """
<style>
[data-testid="stSidebarContent"] {
    color: white;
    background-color: #dcb4cc;
    border-radius: 25px;
    border-style: solid;
    border-width: 7px;
    background-image: url("https://static.vecteezy.com/system/resources/previews/008/359/817/non_2x/beautiful-and-bright-yellow-and-purple-color-gradient-background-combination-soft-and-smooth-texture-free-vector.jpg");
}
</style>
"""
)

# This is to style the main app background
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

# This is to style the header of the app
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
    st.warning("Please first login! Click on our logo to the left to open the sidebar to login!")
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

st.logo("assets/R.D.Y. to Eat.png",icon_image="assets/R.D.Y. to Eat.png")# This is to display the app logo in the header

# An expander holding a welcome message for users 
# This is to create a stylable container that holds the welcome message and styles it
with st.expander("Welcome!"):
    with stylable_container(
                key=f"container_with_bordew2323e23e",
                css_styles=["""
                
                    {
                        border-radius: 0.5rem;
                        background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                        padding: calc(1em - 1px);
                            
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

#This is a container that holds the top rated meals method results and displays it  with 
# specific css styable conatiner coding 

top_rated = topRated()
if top_rated:
    with stylable_container(
                    key=f"container_with_bordew2weewe323e23e",
                    css_styles=["""
                    
                        {
                            border-radius: 0.5rem;
                            background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                            padding: calc(1em - 1px);
                                
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
        
        st.subheader("🌠Top 5 Dishes across Wellesley!")
        for dish in top_rated:
            st.markdown(f"〰️{dish[0]} with a rating of "+ '⭐' * int(dish[1]),help=f"Rating of {dish[1]} ")


#This section of code will display the current meals avaiable in dinning halls based on users current time 
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

    #Subheader to display and section of so users understand what is being displayed here 
    st.subheader("Whats Happening in the Halls right now!")
    st.warning("Please log your meals in the Wellesley Fresh Meals Tab")

    col1,col2=st.columns(2)
     
    options=["Lulu","Bates","Stone D","Tower"]
    with col1:
        fav_option=st.selectbox("Select A Hall!",options)
    with col2:
        st.write("")
        st.write("")
        with st.popover("Dining Hall visits Breakdown! "):
            st.plotly_chart(common_dining(getName()[1]))

    # Setting timezone
    import pytz
    timezone = pytz.timezone('America/New_York') 
    now = datetime.now(timezone)

    date = now.date()
    timenow = now.time()
    current_hour=timenow.hour
    col12,=st.columns(1,vertical_alignment="center")

    #This will filter what to display to the users based on what time it currently is for th euser based on EST time zopne 
    
    #When breakfast display breakfast menus 
    with col12:
        if 5 <= current_hour < 10:
            selected_time="Breakfast"
            st.warning(f"For {selected_time} at {fav_option}")

            #Gets data from the wellsley fresh api and gets the menus as json files 
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
            #Filters data frame to on only display the meal names based on name 
            cleandf= cleandf.loc[(cleandf["date"].str.split("T").str[0]==str(date))]
            if not cleandf.empty:
                for item in cleandf["name"].items():
                    st.write("〰️"+item[1])
            else:
                st.warning("No Meals Available")

        #When lunch display lunch menus 
        elif 10 <= current_hour < 14:
            

            selected_time="Lunch"
            st.warning(f"For {selected_time} at {fav_option}")

            #Gets data from the wellsley fresh api and gets the menus as json files 
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
            #Filters data frame to on only display the meal names based on name 
            cleandf= cleandf.loc[(cleandf["date"].str.split("T").str[0]==str(date))]
            if not cleandf.empty:
                for item in cleandf["name"].items():
                    st.write("〰️"+item[1])
            else:
                st.warning("No Meals Available")
            
        
        #When Dinner display dinner menus         
        elif 14 <= current_hour < 21:
            selected_time="Dinner"
            st.warning(f"For {selected_time} at {fav_option}")

            #Gets data from the wellsley fresh api and gets the menus as json files 
            data = wellesley_fresh_api.wellesleyCall(
                            fav_option, 
                            selected_time, 
                            date)
            df = pd.json_normalize(data)


            st.write(df)    
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
            
            #Filters data frame to on only display the meal names based on name 
            cleandf= cleandf.loc[(cleandf["date"].str.split("T").str[0]==str(date))]
            if df.empty:
                for item in cleandf["name"].items():
                    st.write("〰️"+item[1])
            else:
                st.warning("No Meals Available")
        #Displays this warning when all the dining halls are closed 
        else:
            st.warning("All Dining Halls are closed!")

        

            

