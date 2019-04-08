import os
import io
import time
import yaml

config_file_path = os.environ['HOME'] + "/ctxt_search-config.yml"

def createDefaultConfigFile():
    data = {
        'listen': [
            os.environ['HOME'] + "/Documentos",
            os.environ['HOME'] + "/Músicas",
            os.environ['HOME'] + "/Vídeos",
            os.environ['HOME'] + "/Imagens",
            os.environ['HOME'] + "/Downloads",
            os.environ['HOME']
        ],
        'recursive_listening': False,
        'use_location': True,
        'use_agenda': True
    }

    with io.open(config_file_path, "w", encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    with io.open(config_file_path, "r") as stream:
        data_loaded = yaml.load(stream)
        if(data == data_loaded):
            print("File created successfully") 
            return data
        else:
            print("Warning: there was an error while creating config file")
            return False


def parseConfigFile():
    print("I'll check the config file, located in: ", config_file_path)
    if(os.path.isfile(config_file_path)):
        with open(config_file_path, "r") as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    
    else:
        print("Configuration file doesn't exists, Creating default file")
        return createDefaultConfigFile()
