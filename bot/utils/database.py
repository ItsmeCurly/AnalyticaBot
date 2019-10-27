import sqlite3, re, configparser
from typing import List
from sqlite3 import Error

#from bot.constants import database_path, config_path

def quick_execute_sql_command(*, command, commit = False):
    conn, c = get_cursor()

    c.execute(command)

    (conn.commit(), None)[commit]

    conn.close()

def create_messages_table():
    """creates the messages table"""

    quick_execute_sql_command(
        command='''CREATE TABLE messages
        (id integer primary key,
        member integer,
        content text,
        channel integer,
        guild integer,
        time timestamp)''', commit = True)


def create_userprofiles_table():
    """creates the user profiles table"""

    quick_execute_sql_command(
        command='''CREATE TABLE userprofiles
        (id integer primary key,
        userid integer,
        discriminator integer,
        name text,
        guild_id integer,
        guild_user_display_name text,
        avatarurl text,
        premium_since datetime,
        status text,
        mobile_status text,
        desktop_status text,
        web_status text,
        roles text,
        activity text,
        created_at datetime,
        last_updated timestamp,
        last_online timestamp,
        update_type text)''', commit=True)

def create_serverref_table():
    """creates server reference table"""

    quick_execute_sql_command(
        command='''CREATE TABLE serverref
        (id integer primary key,
        guild_id integer,
        guildname text,
        channel integer,
        channelname text,
        last_channel_update timestamp,
        last_channel_activity timestamp,
        last_guild_update timestamp,
        last_guild_activity timestamp)''', commit=True)

def del_connection(table_name: str) -> None:
    confirm = input(f"This will delete table {table_name}, confirm? (Y/N): ")

    if confirm == 'Y' or confirm == 'y':
        quick_execute_sql_command(command = (f'DROP TABLE {table_name}'), commit=True)
        print(f'{table_name} deleted')
    else:
        return

def check_exists_table(table_name: str) -> None:
    conn, c = get_cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")

    group = c.fetchone()

    conn.close()

    return (group != None and table_name == group[0])

def print_table_structure(table_name: str) -> None:
    conn, c = get_cursor()

    c.execute(f"pragma table_info('{table_name}')")

    print(c.fetchall())

    conn.close()

def pprint_table_structure(table_name: str) -> str:
    conn, c = get_cursor()
    c.execute(f"pragma table_info('{table_name}')")

    _list_structure = c.fetchall()

    _return_str = str(_list_structure[0][1])
    for ele in _list_structure[1:]:
        _return_str = _return_str + " " * 16 + ele[1]

    conn.close()
    return _return_str

def pprint_table_preview(table_name: str) -> list:
    table_structure = pprint_table_structure(table_name)

    table_structure_list = table_structure.split(" ")

    conn, c = get_cursor()
    _str = ""
    for row_message in c.execute(f'SELECT * FROM {table_name} ORDER BY id ASC LIMIT ' + str(5)):
        spacing = table_structure_list[0]
        _str = f"%{spacing}"

    conn.close()


def get_table_structure(table_name: str) -> str:
    conn, c = get_cursor()

    c.execute(f"pragma table_info('{table_name}')")

    _list = c.fetchall()
    conn.close()
    _str = ""

    for ele in _list:
        _str = "|".join([_str, " ".join(str(i) for i in ele)])

    return _str

def check_table_structure(table_name: str) -> bool:
    config = configparser.ConfigParser()
    config.read(filenames = 'config.ini')

    db = config['Database']

    struc = db.get(f'struc_{table_name}')

    if struc == None:
        raise ValueError("Config missing structure schema")

    return get_table_structure(table_name = table_name) == struc

def print_tables() -> list:
    conn, c = get_cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table'")

    _to_return = c.fetchall()

    conn.close()
    return _to_return

def get_cursor() -> (sqlite3.Connection, sqlite3.Cursor):
    conn = sqlite3.connect(database = 'db\\analyticadatapoints.db') #database_path
    return conn, conn.cursor()

if __name__ == "__main__":
    #del_connection(table_name='serverref')
    #del_connection(table_name='userprofiles')

    #create_serverref_table()
    #create_userprofiles_table()

    #print(get_table_structure(table_name='userprofiles'))
    #print(get_table_structure(table_name='serverref'))

    print(pprint_table_structure(table_name='userprofiles'))