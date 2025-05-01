import plotly.express as px
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from Dashboard import clone_private_repo

DB_PATH= clone_private_repo()

conn = sqlite3.connect(DB_PATH)

c = conn.cursor()

def spider_graph(uid):
    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()
    c.execute("SELECT SUM(protein), SUM(fats), SUM(carbohydrates) FROM food_log WHERE uid = ?", (uid, ))

    df = pd.DataFrame(dict(
        r = list(c.fetchone()),
        theta=['Protein (g)','Fats (g)','Carbs (g)']))
    print(df)
    fig = px.line_polar(df,title="Nutritional Breakdown" ,r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
    font=dict(
        color='Purple',
        family='Lexend',
        size=14
    ))
    fig.update_traces(
    fill='toself',
    line=dict(color='rgba(255, 255, 255, 0.8)'),  # Line color (white with some transparency)
    fillcolor='rgba(113, 20, 163, 0.5)'           # Fill color (semi-transparent purple)
)
    return fig

def average_calories_by_meal(uid):

    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()
    c.execute("SELECT meal_type, AVG(calories) FROM food_log WHERE uid = ? GROUP BY meal_type ", (uid, ))
    rows = c.fetchall()

    data = [list(row) for row in rows]
    df = pd.DataFrame(data, columns=['Meal', 'Avg. Calories (kcal)'])
    fig = px.bar(df,title="Avg. Calories", x='Meal', y='Avg. Calories (kcal)')
              # Fill color (semi-transparent purple)
    fig.update_traces(
    marker=dict(color='rgba(113, 20, 163, 0.6)')  # Semi-transparent purple
)
    return fig

def nutrient_breakdown(uid):
    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()
    c.execute("SELECT SUM(protein), SUM(fats), SUM(carbohydrates) FROM food_log WHERE uid = ?", (uid, ))
    row = c.fetchone()
    
    labels = ['Protein', 'Fats', 'Carbs']
    values = [row[0], row[1], row[2]]

    fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=.5,  # To create a donut shape
    marker=dict(colors=[
        '#9B4D9C',  # Light purple for Protein
        '#6A2C9C',  # Medium purple for Fats
        '#3E0E75'   # Dark purple for Carbs
    ]),
)])
   
             # Fill color (semi-transparent purple)
    
    fig.update_layout(
    title='Nutritional Breakdown',  # Optional title
    font=dict(
        color='white',                 # Font color
        family='Lexend',
        size=14
    ),
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Background of the entire figure
    plot_bgcolor='rgba(0, 0, 0, 0)',   # Background of plotting area
)
    return fig

def location_nutrient_breakdown (uid):
    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()
    c.execute("SELECT SUM(protein), SUM(fats), SUM(carbohydrates), location_id FROM food_log WHERE uid = ? GROUP BY location_id", (uid, ))

    rows = c.fetchall()

    data = [list(row) + [sum(row[0:2])] for row in rows]
    df = pd.DataFrame(data, columns=['Protein', 'Fats', 'Carbs', 'Total Nutrients', 'Dining Hall'])

    fig = px.bar_polar(df, r="Total Nutrients", theta="Dining Hall", color="Protein", template="plotly_white",
                color_discrete_sequence= px.colors.sequential.Plasma_r)
    
    return fig

# make visual with calorie count per dining hall, which dining hall we visit the most
# goal graphs

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

    fig = px.bar_polar(df_long, r="Amount", theta="Dining Hall", color="Nutrient", 
                       color_discrete_sequence=["#EF476F", "#FFD166", "#06D6A0"])

    fig.update_layout(
        template="plotly_white",  # Set the template to white
        paper_bgcolor='white',    # Set the background of the whole figure
        plot_bgcolor='white',     # Set the background of the plot area
        font=dict(color='black'), # Set the font color to black (optional)
    )

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
        color_discrete_sequence=["purple"]
    )

    fig.update_layout(yaxis=dict(categoryorder='total ascending'))  # most common at top
    
    return fig

def calorie_goal(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT SUM(f.calories), u.calorie_goal
        FROM food_log f
        JOIN user u ON u.uid = f.uid
        WHERE f.uid = ?
        GROUP BY u.uid
    """, (uid,))

    row = c.fetchone()
    conn.close()

    consumed = row[0]
    goal = row[1]

    if consumed < goal:
        labels = ['Calories Consumed', 'Remaining']
        values = [consumed, goal - consumed]
        colors = ['#FFA07A', '#90EE90']
    elif consumed == goal:
        labels = ['Calories Consumed']
        values = [goal]
        colors = ['#FFA07A']
    else:
        labels = ['Calorie Goal', 'Over Limit']
        values = [goal, consumed - goal]
        colors = ['#FFA07A', '#FF6347']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    fig.update_traces(textinfo='label+percent')
    fig.update_layout(title_text=f"Calorie Tracker: {consumed:.0f} / {goal:.0f} kcal")
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
    conn.close()

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