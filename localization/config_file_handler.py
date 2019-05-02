#!/usr/bin/python3

import os
import io
import time
import yaml

import settings

config_file_path = os.environ['HOME'] + "/ctxt_search-location_plugin.yml"

def createDefaultConfigFile():
    settings.init()
    data = settings.default

    with io.open(config_file_path, "w", encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    with io.open(config_file_path, "r") as stream:
        data_loaded = yaml.load(stream)
        if(data == data_loaded):
            settings.loaded = data_loaded
            return data
        else:
            return False


def parseConfigFile():
    if(os.path.isfile(config_file_path)):
        with open(config_file_path, "r") as stream:
            try:
                settings.loaded = yaml.load(stream)
                return settings.loaded
            except yaml.YAMLError as exc:
                print(exc)
    
    else:
        return createDefaultConfigFile()
