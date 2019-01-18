import configparser


def getConfig(section, option):
    config = configparser.ConfigParser()
    config.read("Config.cnf")
    value = config.get(section, option)
    return value