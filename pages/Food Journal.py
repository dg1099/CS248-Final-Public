import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from userAuth.user_profile import getName
import matplotlib.pyplot as plt
from Data_Visuals.data_visualization_methods import spider_graph, average_calories_by_meal, nutrient_breakdown
from userAuth.user_profile import getName
import sqlite3
from datetime import datetime
from Dashboard import clone_private_repo
import pandas as pd
import subprocess
import plotly.express as px
import pandas as pd
import sqlite3
import plotly.graph_objects as go

st.set_page_config(layout="wide")

DB_PATH= clone_private_repo()

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
        padding: calc(1em - 1px);
        border-radius: 0.5rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
    }
    </style>
""", unsafe_allow_html=True)

##################### UPDATING AND GETTING CALORIE/PROTEIN GOALS ########################
def calorie_goal(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    cal_goal = get_calorie_goal(uid)
    c.execute("""
        SELECT SUM(protein)
        FROM food_log
        WHERE uid = ?
        """, (uid,))
    
    consumed = c.fetchone()[0]

    print(consumed)
    
    if consumed < cal_goal:
        labels = ['Calories Consumed', 'Remaining']
        values = [consumed, cal_goal - consumed]
        colors = ['#FFA07A', '#90EE90']
    elif consumed == cal_goal:
        labels = ['Calories Consumed']
        values = [cal_goal]
        colors = ['#FFA07A']
    else:
        labels = ['Calories Goal', 'Over Limit']
        values = [cal_goal, consumed - cal_goal]
        colors = ['#FFA07A', '#FF6347']

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    fig.update_traces(textinfo='label+percent')
    fig.update_layout(title_text=f"Calorie Tracker: {consumed:.0f} / {cal_goal:.0f} kcal")
    
    return fig

def protein_goal(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT SUM(f.protein), u.protein_goal
        FROM food_log f
        JOIN user u ON u.uid = f.uid
        WHERE f.uid = ?
        GROUP BY u.uid
        """, (uid,))

    row = c.fetchone()

    if row is None or row[0] is None:
        print("No data found.")
        return

    consumed = row[0]
    goal = row[1]

    if consumed < goal:
        labels = ['Protein Consumed', 'Remaining']
        values = [consumed, goal - consumed]
        colors = ['#87CEEB', '#D3D3D3']  # Blue for protein, gray for remaining
    elif consumed == goal:
        labels = ['Protein Consumed']
        values = [goal]
        colors = ['#87CEEB']
    else:
        labels = ['Protein Goal', 'Over Limit']
        values = [goal, consumed - goal]
        colors = ['#87CEEB', '#FF6347']  # Red for excess

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    fig.update_traces(textinfo='label+percent')
    fig.update_layout(title_text=f"Protein Tracker: {consumed:.0f} / {goal:.0f}g")
    return fig

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

def location_nutrient_breakdown (uid):
            # this would work best if only used for the month/all time
            
            conn = sqlite3.connect(DB_PATH)

            c = conn.cursor()
            c.execute("SELECT SUM(protein), SUM(fats), SUM(carbohydrates), location_id FROM food_log WHERE uid = ? GROUP BY location_id", (uid, ))

            rows = c.fetchall()

            df = pd.DataFrame(rows, columns=['Protein (g)', 'Fats (g)', 'Carbs (g)', 'Dining Hall'])

            df_long = pd.melt(
                df,
                id_vars=['Dining Hall'],
                value_vars=['Protein (g)', 'Fats (g)', 'Carbs (g)'],
                var_name='Nutrient',
                value_name='Amount'
            )

            fig = px.bar_polar(df_long, r="Amount", theta="Dining Hall", color="Nutrient", template="plotly_dark",
                        color_discrete_sequence=["#FFB6C1", "#FFDAB9", "#FAFAD2"])
            
            return fig

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


email=getName()[0]


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

   
    with stylable_container(
        key="table3sdsDwe",
        css_styles="""
            {
                background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                border-radius: 0.5rem;
                padding: 1em;
            }
        """,
    ):
        col1,col2,col3=st.columns(3)
        with col1:
            st.write("")
        with col2:
            st.subheader("Whats in your journal!",help="Hover over question marks to display meal calorie amount")
        with col3:
            st.write("")
        #This holds all the meals logged by the user for that specific date selected 
        today = datetime.now().date()
    
    with st.expander("These are the meals you loved ❤️"):
        st.write("")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Replace '123' with your actual uid
        specific_uid = getName()[1]

        # Execute the query
        cursor.execute("""
            SELECT uid, emotion, comment,meal
            FROM rating
            WHERE emotion = 'Love' AND uid = ?
        """, (specific_uid,))

        # Fetch and print results
        results = cursor.fetchall()
        cols1,cols2,cols3=st.columns([1, 2, 2])
        for (name,emotion,comment,meal) in results:
            with cols1:
                st.write("💕")
            with cols2:
                st.write(meal)
            with cols3:
                st.write(comment)
            

        # Clean up
        cursor.close()
        conn.close()


    

    #This loads all the lists so they they later display all the meals based on the dayes they where served 
    daily,weekly,monthly=st.tabs(["Daily Meal Log","Weekly Meal Log","Monthly Meal Log"])
    
    with daily: 
            with stylable_container(
        key="table3wqew",
        css_styles="""
            {
                background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                border-radius: 0.5rem;
                padding: 1em;
            }
        """,
    ): 
                today=st.date_input("Select A Date", today)
                uid = getName()[1]
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
                snack=[]

                for item in meals_today:
                    if item[4]=="Breakfast":
                        breakfast.append(item)
                    elif item[4]=="Lunch":
                        lunch.append(item)
                    elif item[4]=="Dinner":
                        dinner.append(item)
                    else:
                        snack.append(item)


            
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

                st.subheader("Snack",divider=True)
                if len(snack)==0:
                    st.write("Nothing was logged")
                for food4 in snack: 
                    st.markdown(food4[5],help=f"Calories in Meal: {food4[6]}")


        #Make a double for loop to loop from the specific date range and they display all the meals for all the days 
    import datetime
    with weekly:
        with stylable_container(
        key="table3we",
        css_styles="""
            {
                background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                border-radius: 0.5rem;
                padding: 1em;
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
            c.execute(
                """SELECT * FROM food_log WHERE date(date) BETWEEN ? AND ? AND uid = ?""",
                (d[0], d[1], uid)
            )
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
                background-image: linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%);
                border-radius: 0.5rem;
                padding: 1em;
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
            c.execute(
                """SELECT * FROM food_log WHERE date(date) BETWEEN ? AND ? AND uid = ?""",
                (d[0], d[1], uid)
            )
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

    with headCol2:
        with st.popover("Meal Goals",use_container_width=True):
            calorieGoal=st.slider("Calorie Goals:", 1,3000)
            proteinGoal=st.slider("Protein Goals:", 1,150)

            st.session_state["calorieGoal"]=calorieGoal
            st.session_state["protienGoal"]=proteinGoal

            #Current Values
            current_calorie_goal = get_calorie_goal(getName()[1])
            current_protein_goal = get_protein_goal(getName()[1])
            
            #Update the database if the goals have changed
            if calorieGoal != current_calorie_goal:
                change_calorieGoal(username, calorieGoal)
            if proteinGoal != current_protein_goal:
                change_proteinGoal(username, proteinGoal)


            goals={
            "Calories Goal": st.session_state["calorieGoal"],
            "Protein Goal": st.session_state["protienGoal"]
        }
            colprotien,colcalorie,colcarbs=st.columns(3)
            
    with st.expander("See you Calorie and Protien Goals"):
        col1,col2=st.columns(2)
        with col1:
            st.plotly_chart(calorie_goal(getName()[1]))
        with col2:
            st.plotly_chart(protein_goal(getName()[1]))
    with st.expander("Visualize Your Nutrients Breakdown"):
        st.plotly_chart(location_nutrient_breakdown (getName()[1]))
    
    with st.expander("Average Calories Per Meal Category"):
        plot2=average_calories_by_meal(email[1])
        st.plotly_chart(plot2,use_container_width=True)
    with st.expander("Where can you been found on campus!"):
        st.plotly_chart(common_dining(getName()[1]))
    
    
   
    
        


