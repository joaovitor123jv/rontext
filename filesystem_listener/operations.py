import subprocess
import settings


def createdSomething(type_names):
    return True if (type_names[0] == "IN_MOVED_TO" or type_names[0] == "IN_CREATE") else False

def deletedSomething(type_names):
    return True if (type_names[0] == "IN_MOVED_FROM" or type_names[0] == "IN_DELETE") else False

def callIcsPlugin(file):
    return_data = subprocess.run([settings.loaded['ics_parser_bin'], file], stdout=subprocess.PIPE)

    print(return_data.stdout)

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