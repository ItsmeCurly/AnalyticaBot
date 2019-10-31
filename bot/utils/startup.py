import configparser
import os
import webbrowser
from os import path

import bot.utils.database as db
from bot.constants import CONFIG_PATH, DATABASE_PATH, PREFIXES_PATH

tables = ["messages", "serverref", "userprofiles"]
table_creation = [db.create_messages_table, db.create_serverref_table, db.create_userprofiles_table]

def main() -> None:
    #create config file

    if not path.exists(CONFIG_PATH):
        create_config(CONFIG_PATH)

    #create dbs

    if not path.exists(DATABASE_PATH):
        pass
        #create db somehow

    """ for i in range(len(tables)):
        if not db.check_exists_table(table_name = tables[i]) or not db.check_table_structure(table_name = tables[i]):
            table_creation[i]() """

    #create prefixes json
    if not path.exists(PREFIXES_PATH):
        pass
        #create json file

def read_token() -> str:
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    token = cfg['Token']['token']

    if token == None:
        raise ValueError("No token supplied in config, please supply a token")

    return cfg['Token']['token']

if __name__ == "__main__":
    main()
