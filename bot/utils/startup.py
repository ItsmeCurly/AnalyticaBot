import configparser
import os
import webbrowser
from os import path

import bot.utils.database as db
from bot.constants import config_path, database_path, prefixes_path

tables = ["messages", "serverref", "userprofiles"]
table_creation = [db.create_messages_table, db.create_serverref_table, db.create_userprofiles_table]

def main() -> None:
    #create config file

    if not path.exists(config_path):
        create_config(config_path)

    #create dbs

    if not path.exists(database_path):
        pass
        #create db somehow

    """ for i in range(len(tables)):
        if not db.check_exists_table(table_name = tables[i]) or not db.check_table_structure(table_name = tables[i]):
            table_creation[i]() """

    #create prefixes json
    if not path.exists(prefixes_path):
        pass
        #create json file

def create_config(config_path) -> None:
    cfg = configparser.ConfigParser()
    cfg['General'] = {}

    cfg['Token'] = {}
    cfg['Token']['token'] = ""

    cfg['Database'] = {}
    dbs = cfg['Database']

    dbs['struc_messages'] = r"""|0 id integer 0 None 1|1 member integer 0 None 0
    |2 content text 0 None 0|3 channel integer 0 None 0|4 guild integer 0 None 0
    |5 time timestamp 0 None 0"""
    
    dbs['struc_userprofiles'] = r"""|0 id integer 0 None 1|1 userid integer 0 
    None 0|2 name text 0 None 0|3 guild_id integer 0 None 0|4 guild_user_name 
    text 0 None 0|5 avatar_url text 0 None 0|6 created_at datetime 0 None 0|7 
    last_updated timestamp 0 None 0|8 last_online timestamp 0 None 0"""
    
    dbs['struc_serverref'] = r"""|0 id integer 0 None 1|1 guild_id integer 0 
    None 0|2 guildname text 0 None 0|3 channel integer 0 None 0|4 channelname 
    text 0 None 0|5 last_channel_update timestamp 0 None 0|6 
    last_channel_activity timestamp 0 None 0|7 last_guild_update timestamp 0 
    None 0|8 last_guild_activity timestamp 0 None 0"""

    with open(config_path, 'w') as config_file:
            cfg.write(config_file)

def read_token() -> str:
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    token = cfg['Token']['token']

    if token == None:
        raise ValueError("No token supplied in config, please supply a token")

    return cfg['Token']['token']

if __name__ == "__main__":
    main()
