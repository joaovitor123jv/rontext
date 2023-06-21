#!/usr/bin/python3

import os
import io
import yaml

import settings


config_file_path = os.environ['HOME'] + "/.ctxt_search-localization_plugin.yml"


def createDefaultConfigFile():
    settings.init()
    data = settings.default

    with io.open(config_file_path, "w", encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    with io.open(config_file_path, "r") as stream:
        data_loaded = yaml.load(stream, Loader=yaml.Loader)
        if(data == data_loaded):
            settings.loaded = data_loaded
            return data
        else:
            return False


def parseConfigFile():
    if(os.path.isfile(config_file_path)):
        with open(config_file_path, "r") as stream:
            try:
                settings.loaded = yaml.load(stream, Loader=yaml.Loader)
                return settings.loaded
            except yaml.YAMLError as exc:
                print(exc)
    
    else:
        return createDefaultConfigFile()
