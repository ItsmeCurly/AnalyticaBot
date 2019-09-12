import sqlite3
from sqlite3 import Error

def create_connection(db_loc, db_filename):

    conn = sqlite3.connect(db_loc + "\\" + db_filename)
    c = conn.cursor()

    c.execute('''CREATE TABLE messages
                (id integer primary key,
                member integer, content text, channel integer, guild integer, time timestamp)''')

    conn.commit()

    conn.close()


def del_connection(db_loc, db_filename):

    conn = sqlite3.connect(db_loc + "\\" + db_filename)
    c = conn.cursor()

    c.execute('''DROP TABLE messages''')

    # Save (commit) the changes
    conn.commit()

    conn.close()
def test_connect(db_loc, db_filename):
    conn = sqlite3.connect(db_loc + "\\" + db_filename)
    c = conn.cursor()

    for row in c.execute('SELECT * FROM messages ORDER BY id'):
        print (row)

    conn.close()

if __name__ == "__main__":
    test_connect("E:\\Programs\\db", "analyticaDataPoints.db")
