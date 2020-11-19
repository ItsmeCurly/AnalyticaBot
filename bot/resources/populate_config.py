import configparser
import sys

sys.path.insert(1, 'C:/Users/adamg/Documents/GitHub/AnalyticaBot')

from bot.constants import CONFIG_PATH

def create_config():
    cfg = configparser.ConfigParser()
    cfg['General'] = {}

    cfg['Token'] = {}
    cfg['Token']['token'] = ""

    cfg['Database'] = {}
    dbs = cfg['Database']

    dbs['database_loc'] = 'db\\analyticaDataPoints.db'
    dbs['struc_messages'] = r"""|0 id integer 0 None 1|1 member integer 0 None 0|2 content text 0 None 0|3 channel integer 0 None 0|4 guild integer 0 None 0|5 time timestamp 0 None 0"""
    dbs['struc_userprofiles'] = r"""|0 id integer 0 None 1|1 userid integer 0 None 0|2 name text 0 None 0|3 avatarurl text 0 None 0|4 last_updated timestamp 0 None 0|5 last_online timestamp 0 None 0"""
    dbs['struc_serverref'] = r"""|0 id integer 0 None 1|1 guild integer 0 None 0|2 guildname text 0 None 0|3 channel integer 0 None 0|4 channelname text 0 None 0|5 last_updated timestamp 0 None 0|6 last_activity timestamp 0 None 0"""

    print(cfg)

    with open(CONFIG_PATH, 'w') as config_file:
        cfg.write(config_file)

if __name__ == "__main__":
    create_config()