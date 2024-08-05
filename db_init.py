import sqlite3 as sql

def db_init():
    conn = sql.connect('trade_history.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trades'")
    table_exists = c.fetchone()
    if not table_exists:
        print("Creating 'trades' table...")
    c.execute('''CREATE TABLE IF NOT EXISTS trades
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT, 
                time TEXT, 
                price REAL, 
                quantity REAL, 
                type TEXT, 
                ticker TEXT,
                bot TEXT);''')
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    db_init()