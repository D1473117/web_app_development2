import sqlite3
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()
cursor.execute("SELECT id, amount, type FROM transactions ORDER BY id DESC LIMIT 5")
rows = cursor.fetchall()
for r in rows:
    print(r)
conn.close()
