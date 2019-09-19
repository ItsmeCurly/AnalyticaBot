import sqlite3
from sqlite3 import Error

#TODO: CONFIG
database = "E:\\Programs\\db\\analyticaDataPoints.db"

def execute_sql_command(command, *, commit = False):
    conn, c = get_cursor()

    c.execute(command)

    if commit:
        conn.commit()
    conn.close()

def create_messages_table():
    execute_sql_command('''CREATE TABLE messages
                (id integer primary key,
                member integer, content text, channel integer, guild integer, time timestamp)''', commit = True)


def create_userprofiles_table():
    execute_sql_command('''CREATE TABLE userprofiles
                (id integer primary key, userid integer, name text, avatarurl text)''', commit=True)

def create_serverref_table():
    execute_sql_command('''CREATE TABLE serverref
                (guild integer, guildname text, channel integer, channelname text, last_updated timestamp)''', commit=True)

def del_connection(db_loc, db_filename):
    execute_sql_command('''DROP TABLE messages''', commit = True)

def test_connect(db_loc, db_filename):
    conn, c = get_cursor()

    for row in c.execute('SELECT * FROM messages ORDER BY id desc LIMIT 1000'):
        print (row)

    conn.close()

def test_check_exists(table_name):
    execute_sql_command(
        (f"SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'", table_name))

def get_cursor():
    conn = sqlite3.connect(database)
    return conn, conn.cursor()

if __name__ == "__main__":
    pass
