import configparser, webbrowser, database as db
from os import path

CONFIG_PATH = 'config.ini'

tables = ["messages", "serverref", "userprofiles"]
table_creation = [db.create_messages_table, db.create_serverref_table, db.create_userprofiles_table]

if __name__ == "__main__":
    #create config file
    if not path.exists(CONFIG_PATH):
        cfg = configparser.ConfigParser()
        cfg['General'] = {}
        cfg['Token'] = {}
        cfg['Token']['token'] = ""
        cfg['Database'] = {}
        dbs = cfg['Database']
        dbs['struc_messages'] = r"""|0 id integer 0 None 1|1 member integer 0 None 0|2 content text 0 None 0|3 channel integer 0 None 0|4 guild integer 0 None 0|5 time timestamp 0 None 0"""
        dbs['struc_userprofiles'] = r"""|0 id integer 0 None 1|1 userid integer 0 None 0|2 name text 0 None 0|3 avatarurl text 0 None 0|4 last_updated timestamp 0 None 0|5 last_online timestamp 0 None 0"""

        with open(CONFIG_PATH, 'w') as config_file:
            cfg.write(config_file)

    #create dbs
    """if not db.check_exists_table("messages") or not db.check_table_structure("messages"):
        db.create_messages_table()
    if not db.check_exists_table("serverref") or not db.check_table_structure("serverref"):
        db.create_serverref_table()"""

    if not db.check_exists_table("userprofiles") or not db.check_table_structure("userprofiles"):
        db.create_userprofiles_table()
        
    for i in range(len(tables)):
        if not db.check_exists_table(tables[i]) or not db.check_table_structure(tables[i]):
            table_creation[i]()
