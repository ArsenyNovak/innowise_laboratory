import sqlite3

with sqlite3.connect('school.db') as conn:
    cursor = conn.cursor()

    with open('script.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    conn.commit()