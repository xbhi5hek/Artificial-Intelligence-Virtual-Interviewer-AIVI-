import sqlite3

def get_connection():
    conn = sqlite3.connect('aivi.db')
    return conn