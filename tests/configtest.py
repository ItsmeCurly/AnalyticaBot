import configparser
if __name__ == "__main__":
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    print(cfg.sections()[1])