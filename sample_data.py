# SQL testing 

import sqlite3

conn = sqlite3.connect("App Version 1/food_tracker.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM food_log")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
