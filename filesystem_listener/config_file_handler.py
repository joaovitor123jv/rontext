import os
import io
import time
import json

import settings


config_file_path = os.environ['HOME'] + "/.ctxt_search-config.json"


def createDefaultConfigFile():
    settings.init()
    data = settings.default

    with io.open(config_file_path, "w", encoding='utf8') as outfile:
        json.dump(data, outfile, indent=4)

    with io.open(config_file_path, "r") as stream:
        data_loaded = json.load(stream)
        if(data == data_loaded):
            print("File created successfully, adding to settings")
            settings.loaded = data_loaded
            return data
        else:
            print("Warning: there was an error while creating config file")
            return False


def parseConfigFile():
    print("I'll check the config file, located in: ", config_file_path)
    if(os.path.isfile(config_file_path)):
        with open(config_file_path, "r") as stream:
            try:
                settings.loaded = json.load(stream)
                settings.runtime = {}
                return settings.loaded
            except json.JSONDecodeError as exc:
                print(exc)

    else:
        print("Configuration file doesn't exists, Creating default file")
        return createDefaultConfigFile()
