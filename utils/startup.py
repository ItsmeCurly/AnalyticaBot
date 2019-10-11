import configparser, webbrowser
from os import path

CONFIG_PATH = 'config.ini'

if __name__ == "__main__":
    #create config file
    if not path.exists(CONFIG_PATH):
        cfg = configparser.ConfigParser()
        cfg['General'] = {}
        cfg['Token'] = {}
        cfg['Token']['token'] = ""
        cfg['Database'] = {}
        dbs = cfg['Database']
        dbs['struc_messages'] = r"""[(0, 'id', 'integer', 0, None, 1), (1, 'member', 'integer', 0, None, 0), (2, 'content', 'text', 0, None, 0), (3, 'channel', 'integer', 0, None, 0), (4, 'guild', 'integer', 0, None, 0), (5, 'time', 'timestamp', 0, None, 0)]"""

        with open(CONFIG_PATH, 'w') as config_file:
            cfg.write(config_file)

    #create dbs
    

