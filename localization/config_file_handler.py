#!/usr/bin/python3

import os
import io
import json

import settings


config_file_path = os.environ['HOME'] + "/.ctxt_search-localization_plugin.json"


def createDefaultConfigFile():
    settings.init()
    data = settings.default

    with io.open(config_file_path, "w", encoding='utf8') as outfile:
        json.dump(data, outfile, indent=4)

    with io.open(config_file_path, "r") as stream:
        data_loaded = json.load(stream)
        if(data == data_loaded):
            settings.loaded = data_loaded
            return data
        else:
            return False


def parseConfigFile():
    if(os.path.isfile(config_file_path)):
        with open(config_file_path, "r") as stream:
            try:
                settings.loaded = json.load(stream)
                return settings.loaded
            except json.JSONDecodeError as exc:
                print(exc)
    
    else:
        return createDefaultConfigFile()
