import configparser
import os
import webbrowser
from os import path

import bot.utils.database as db
from bot.constants import CONFIG_PATH, DATABASE_PATH, PREFIXES_PATH

tables = ["messages", "serverref", "userprofiles"]
table_creation = [db.create_messages_table, db.create_serverref_table, db.create_userprofiles_table]

def read_token() -> str:
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    token = cfg['Token']['token']

    if token == None:
        raise ValueError("No token supplied in config, please supply a token")
    
    return cfg['Token']['token']