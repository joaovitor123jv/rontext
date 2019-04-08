import os
import io
import time
import yaml

import settings

config_file_path = os.environ['HOME'] + "/ctxt_search-config.yml"

def createDefaultConfigFile():
    # data = {
    #     'listen': [
    #         os.environ['HOME'] + "/Documentos",
    #         os.environ['HOME'] + "/Música",
    #         os.environ['HOME'] + "/Vídeos",
    #         os.environ['HOME'] + "/Imagens",
    #         os.environ['HOME'] + "/Downloads",
    #         os.environ['HOME']
    #     ],
    #     'recursive_listening': False,
    #     'ignore_hidden': True,
    #     'use_location': True,
    #     'ics_parser_bin': "/home/joaovitor/Documentos/UFG-CDC/PFC/PFC2/Sistema/ics_parser/arquivo.ics",
    #     'use_agenda': True
    # }
    settings.init()
    data = settings.default

    with io.open(config_file_path, "w", encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    with io.open(config_file_path, "r") as stream:
        data_loaded = yaml.load(stream)
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
                settings.loaded = yaml.load(stream)
                return settings.loaded
            except yaml.YAMLError as exc:
                print(exc)
    
    else:
        print("Configuration file doesn't exists, Creating default file")
        return createDefaultConfigFile()
