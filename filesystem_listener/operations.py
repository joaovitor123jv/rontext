import subprocess
import yaml
from io import StringIO
import settings

def createdSomething(type_names):
    return True if (type_names[0] == "IN_MOVED_TO" or type_names[0] == "IN_CREATE") else False

def deletedSomething(type_names):
    return True if (type_names[0] == "IN_MOVED_FROM" or type_names[0] == "IN_DELETE") else False

def parse_yaml_string(string):
    fd = StringIO(string) # Cria um 'arquivo' em memória
    return yaml.load(fd) # Faz o parse do yaml

def callIcsPlugin(file):
    return_data = subprocess.run([settings.loaded['ics_parser_bin'], file], stdout=subprocess.PIPE)

    parsed_return = parse_yaml_string(return_data.stdout.decode('utf8'))

    print(parsed_return[1])

def handleFileCreated(path, filename):
    file = path + '/' + filename
    print("Created file, ", file)

    if(filename.endswith('.ics')):
        print("\t\tCALENDAR FILE DETECTED!!! == ", file)
        callIcsPlugin(file)

def handleFileDeleted(path, filename):
    file = path + '/' + filename
    print("Deleted file ", file)

    if(filename.endswith('.ics')):
        print("\t\tCALENDAR FILE DETECTED!!! == ", file)
        # callIcsPlugin(file)