import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("App Version 1/Menus Csv's/coop.db")
cursor = conn.cursor()

# Execute a query to retrieve all rows from the ingredients table
cursor.execute("SELECT * FROM ingredients")

# Fetch all rows from the query result
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()