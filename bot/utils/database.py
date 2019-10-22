import sqlite3, re, configparser
from sqlite3 import Error

#TODO: CONFIG
database = "db\\analyticaDataPoints.db"
CONFIG_PATH = 'config.ini'

def quick_execute_sql_command(command, *, commit = False):
    conn, c = get_cursor()

    c.execute(command)

    if commit:
        conn.commit()
    conn.close()

def create_messages_table():
    """creates the messages table"""

    quick_execute_sql_command('''CREATE TABLE messages
                (id integer primary key,
                member integer, content text, channel integer, guild integer, time timestamp)''', commit = True)


def create_userprofiles_table():
    """creates the user profiles table"""

    quick_execute_sql_command('''CREATE TABLE userprofiles
                (id integer primary key, userid integer, name text, avatarurl text, last_updated timestamp, last_online timestamp)''', commit=True)

def create_serverref_table():
    """creates server reference table"""

    quick_execute_sql_command('''CREATE TABLE serverref
                (id integer primary key, guild integer, guildname text, channel integer, channelname text, last_updated timestamp, last_activity timestamp)''', commit=True)

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

    group = c.fetchone()

    conn.close()

    return (group != None and table_name == group[0])

def print_table_structure(table_name):
    conn, c = get_cursor()

    c.execute(f"pragma table_info('{table_name}')")

    print(c.fetchall())

    conn.close()

def get_table_structure(table_name):
    conn, c = get_cursor()

    c.execute(f"pragma table_info('{table_name}')")

    _list = c.fetchall()
    conn.close()
    _str = ""

    for ele in _list:
        _str = "|".join([_str, " ".join(str(i) for i in ele)])

    return _str

def check_table_structure(table_name):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    db = config['Database']

    struc = db.get(f'struc_{table_name}')

    if struc == None:
        raise ValueError("Config missing structure schema")

    return get_table_structure(table_name) == struc

def print_tables():
    conn, c = get_cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table'")

    print(c.fetchall())

    conn.close()

def get_cursor():
    conn = sqlite3.connect(database)
    return conn, conn.cursor()

if __name__ == "__main__":
    pass