from database.db import get_connection

def save_result(username, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO results (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()