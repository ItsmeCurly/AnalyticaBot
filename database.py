import sqlite3
from sqlite3 import Error

def create_connection(db_loc, db_filename):
    conn = None
    try:
        conn = sqlite3.connect(db_loc + "\\" + db_filename)
        print(sqlite3.version)
        conn.execute('''CREATE TABLE CLIENTS
             ([generated_id] INTEGER PRIMARY KEY,[Client_Name] text, [Country_ID] integer, [Date] date)''')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_connection("E:\\Programs\\db", "analyticaDataPoints.db")
