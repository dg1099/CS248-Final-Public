import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from userAuth.user_profile import getName
import matplotlib.pyplot as plt
from Data_Visuals.data_visualization_methods import spider_graph, average_calories_by_meal, nutrient_breakdown
from userAuth.user_profile import getName
import sqlite3
from datetime import datetime
from Dashboard import clone_private_repo

import subprocess
import subprocess

def push_changes_to_repo(clone_dir, commit_message="Update database"):
    # Stage all changes
    subprocess.run(["git", "-C", clone_dir, "add", "."], check=True)

    # Check if there are any staged changes
    result = subprocess.run(
        ["git", "-C", clone_dir, "diff", "--cached", "--quiet"],
        capture_output=True
    )

    if result.returncode == 0:
        # No changes to commit
        print("No changes to commit.")
        return

    # Commit and push
    subprocess.run(["git", "-C", clone_dir, "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "-C", clone_dir, "push"], check=True)





DB_PATH= clone_private_repo()
st.set_page_config(layout="wide")

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
    background-image: url("https://images.unsplash.com/photo-1686593686409-43456910d65c?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8cHVycGxlJTIwYmFja2dyb3VuZHxlbnwwfHwwfHx8MA%3D%3D");
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
        background-image: url("https://images.unsplash.com/photo-1686593686409-43456910d65c?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8cHVycGxlJTIwYmFja2dyb3VuZHxlbnwwfHwwfHx8MA%3D%3D");
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

##################### UPDATING AND GETTING CALORIE/PROTEIN GOALS ########################
def change_calorieGoal(username, calorieGoal):
    if isinstance(username, tuple):
        username = username[0]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE user SET calorie_goal = ? WHERE username = ?",
            (calorieGoal, username)
        )
        conn.commit()
        print("Calorie Goal updated successfully.")
    except sqlite3.Error as e:
        print("An error occurred:", e)
    finally:
        conn.close()

def change_proteinGoal(username, proteinGoal):
    if isinstance(username, tuple):
        username = username[0]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE user SET protein_goal = ? WHERE username = ?",
            (proteinGoal, username)
        )
        conn.commit()
        print("Protein Goal updated successfully.")
    except sqlite3.Error as e:
        print("An error occurred:", e)
    finally:
        conn.close()


def get_calorie_goal(username):
    if isinstance(username, tuple):
        username = username[0]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT calorie_goal FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    finally:
        conn.close()

def get_protein_goal(username):
    if isinstance(username, tuple):
        username = username[0]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT protein_goal FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    finally:
        conn.close()

#----------------------------PAGE LAYOUT------------------------------------#


email=getName()


if "access_token" not in st.session_state:
    st.warning("Please first login!")
    #Stop from everything else from being loaded up if they have not loggedin 
else: 

    headCol1,headCol2=st.columns([8,2])

    #This is our header column so we can also have a popout section for prefrences
    with headCol1:
        st.subheader(f"Hello, {getName()[0]}",divider=True)
    username = getName()[1]
    print(username)
    #current_calorie_goal = get_calorie_goal(username)
    #current_protein_goal = get_protein_goal(username)

   

    st.subheader("Whats in your journal!",help="Hover over question marks to display meal calorie amount")
    #This holds all the meals logged by the user for that specific date selected 
    today = datetime.now().date()
    

    

    #This loads all the lists so they they later display all the meals based on the dayes they where served 
    daily,weekly,monthly=st.tabs(["Daily Meal Log","Weekly Meal Log","Monthly Meal Log"])
    
    with daily: 
            with stylable_container(
        key="table3wqew",
        css_styles="""
            {
                border: 4px solid black;
                background: linear-gradient(90deg, rgba(184, 153, 39, 1) 0%, rgba(113, 20, 163, 1) 91%);
                border-radius: 0.5rem;
                padding: 1em;
                color: white; /* Optional: make text easier to see */
            }
        """,
    ): 
                today=st.date_input("Select A Date", today)
                uid = getName()[1]
                st.write(username)
                conn=sqlite3.connect(DB_PATH)
                c=conn.cursor()
                c.execute(
                    """SELECT * FROM food_log WHERE date(date) = ? AND uid = ?""",
                    (today, uid)
                )
                meals_today = c.fetchall()
                rows = c.fetchall() 
                c.close()
                
                breakfast=[]
                lunch=[]
                dinner=[]

                for item in meals_today:
                    if item[4]=="Breakfast":
                        breakfast.append(item)
                    elif item[4]=="Lunch":
                        lunch.append(item)
                    else:
                        dinner.append(item)


            
                st.subheader("Breakfast",divider=True)
                if len(breakfast)==0:
                        st.write("Nothing was logged")
                for food in breakfast: 
                    st.markdown(food[5],help=f"Calories in Meal: {food[6]}")
                    
                
                st.subheader("Lunch",divider=True)
                if len(lunch)==0:
                    st.write("Nothing was logged")
                for food2 in lunch: 
                    st.markdown(food2[5],help=f"Calories in Meal: {food2[6]}")

                st.subheader("Dinner",divider=True)
                if len(dinner)==0:
                    st.write("Nothing was logged")
                for food3 in dinner: 
                    st.markdown(food3[5],help=f"Calories in Meal: {food3[6]}")


        #Make a double for loop to loop from the specific date range and they display all the meals for all the days 
    import datetime
    with weekly:
        with stylable_container(
        key="table3we",
        css_styles="""
            {
                border: 4px solid black;
                background: linear-gradient(90deg, rgba(184, 153, 39, 1) 0%, rgba(113, 20, 163, 1) 91%);
                border-radius: 0.5rem;
                padding: 1em;
                color: white; /* Optional: make text easier to see */
            }
        """,
    ):      
            st.warning("This log only displays days where meals were logged!")
            #This makes it so that th euser can only select one week at a time here 
            start = today - datetime.timedelta(days=7) 
            end = today

            d = st.date_input(
                "Select Date Timeline!",
                value=(start,end),
                
                
            )

            if len(d)!=2:
                st.warning("Please Select a proper date range!")
                st.stop()


            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(""" SELECT * FROM food_log WHERE date(date) BETWEEN ? AND ? """, (d[0], d[1]))
            data=c.fetchall()
            c.close()

            #So we can mange which dates we have in this range 
            dates=[]

            for item in data:
                if item[2] not in dates:
                    dates.append(item[2])
        

            for date in dates: 
                date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                st.subheader(date_obj.strftime('%A'),divider=True)
                for item in data:
                    if item[2]==date:
                        st.markdown(item[5],help=f"Calories in Meal: {item[6]}")
    with monthly:
        with stylable_container(
        key="table3wwerwe",
        css_styles="""
            {
                border: 4px solid black;
                background: linear-gradient(90deg, rgba(184, 153, 39, 1) 0%, rgba(113, 20, 163, 1) 91%);
                border-radius: 0.5rem;
                padding: 1em;
                color: white; /* Optional: make text easier to see */
            }
        """,
    ):      
            st.warning("This log only displays months where meals were logged!")
            #This makes it so that th euser can only select one week at a time here 
            start = today - datetime.timedelta(days=30)
            end = today

            d = st.date_input(
                "Select Date Timeline!",
                value=(start,end),key="Monthly")

            if len(d)!=2:
                st.warning("Please Select a proper date range!")
                st.stop()


            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(""" SELECT * FROM food_log WHERE date(date) BETWEEN ? AND ? """, (d[0], d[1]))
            data=c.fetchall()
            c.close()

            #So we can mange which dates we have in this range 
            months=[]

            for item in data:
                date_obj = datetime.datetime.strptime(item[2], '%Y-%m-%d')
                month=date_obj.strftime('%B')
                if month not in months:
                    months.append(month)

            for date in months: 
                st.subheader(date,divider=True)
                for item in data:
                    date_obj = datetime.datetime.strptime(item[2], '%Y-%m-%d')
                    month=date_obj.strftime('%B')
                    if month==date:
                        st.markdown(item[5],help=f"Calories in Meal: {item[6]}")



    with st.expander("See your graphs!"):
        with headCol2:
            with st.popover("Meal Goals",use_container_width=True):
                calorieGoal=st.slider("Calorie Goals:", 1,3000)
                proteinGoal=st.slider("Protein Goals:", 1,150)

                st.session_state["calorieGoal"]=calorieGoal
                st.session_state["protienGoal"]=proteinGoal

                # Update the database if the goals have changed
                #if calorieGoal != current_calorie_goal:
                    #change_calorieGoal(username, calorieGoal)
                #if proteinGoal != current_protein_goal:
                    #change_proteinGoal(username, proteinGoal)

        goals={
        "Calories Goal": st.session_state["calorieGoal"],
        "Protein Goal": st.session_state["protienGoal"]
    }
        colprotien,colcalorie,colcarbs=st.columns(3)
        
        with colprotien:
            st.subheader("Nutrients Level")
            with stylable_container(
        key="container_with_border_plot",
        css_styles=[
            """
            {
                border: 6px solid black;
                border-radius: 1rem;
                background-color: white;
            }
            """
        ]
    ):
                plot=spider_graph(email[1])
                st.plotly_chart(plot,use_container_width=True)
        with colcalorie:
            st.subheader("Average Cals by meal")
            with stylable_container(
        key="container_with_border_plotsd",
        css_styles=[
            """
            {
                border: 6px solid black;
                border-radius: 1rem;
                background-color: white;
            }
            """
        ]
    ):
                plot2=average_calories_by_meal(email[1])
                st.plotly_chart(plot2,use_container_width=True)

        with colcarbs:
            st.subheader("Nutrient Breakdown")
            with stylable_container(
        key="container_with_border_plowwet",
        css_styles=[
            """
            {
                border: 6px solid black;
                border-radius: 1rem;
                background-color: black;
            }
            """
        ]
    ):
                
                fig=nutrient_breakdown(email[1])
                st.plotly_chart(fig)

push_changes_to_repo("/tmp/private_repo", commit_message="Add new food log entry")       

