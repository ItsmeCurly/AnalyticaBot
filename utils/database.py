import sqlite3
from sqlite3 import Error

#TODO: CONFIG
database = "db\\analyticaDataPoints.db"

def quick_execute_sql_command(command, *, commit = False):
    conn, c = get_cursor()

    c.execute(command)

    if commit:
        conn.commit()
    conn.close()

def create_messages_table():
    quick_execute_sql_command('''CREATE TABLE messages
                (id integer primary key,
                member integer, content text, channel integer, guild integer, time timestamp)''', commit = True)


def create_userprofiles_table():
    quick_execute_sql_command('''CREATE TABLE userprofiles
                (id integer primary key, userid integer, name text, avatarurl text)''', commit=True)

def create_serverref_table():
    quick_execute_sql_command('''CREATE TABLE serverref
                (guild integer, guildname text, channel integer, channelname text, last_updated timestamp)''', commit=True)

def del_connection(table_name):
    quick_execute_sql_command(f'DROP TABLE {table_name}', commit=True)

def test_connect():
    conn, c = get_cursor()

    for row in c.execute('SELECT * FROM messages ORDER BY id desc LIMIT 10'):
        print (row)

    conn.close()

def check_exists_table(table_name):
    conn, c = get_cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    
    print(c.fetchall())
    
    conn.close()
    
def check_table_structure(table_name):
    conn, c = get_cursor()

    c.execute(f"pragma table_info('{table_name}')")

    print(c.fetchall())

    conn.close()
    
def print_tables():
    conn, c = get_cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table'")

    print(c.fetchall())

    conn.close()
    
def get_cursor():
    conn = sqlite3.connect(database)
    return conn, conn.cursor()

if __name__ == "__main__":
    check_table_structure('messages')
