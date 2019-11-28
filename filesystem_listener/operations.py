import subprocess
import settings
import time_parser
import time
import database
import helpers
import os

def isProjectRelated(path):
    return (
        path.startswith( os.environ['HOME'] + "/Documentos/UFG-CDC/PFC/PFC2/Sistema" )
        or
        path.startswith( os.environ['HOME'] + "/.ctxt_search-")
    )

def shouldIgnore(path):
    if isProjectRelated(path):
        return True
    for ignored_substring in settings.loaded['ignore_occurrences']:
        if ignored_substring in path:
            return True
    return False

def created_something(type_names, path):
    return True if (type_names[0] in ["IN_MOVED_TO", "IN_CREATE"]) and not shouldIgnore(path) else False

def accessed_something(type_names, path):
    return True if (type_names[0] == "IN_OPEN") and not shouldIgnore(path) else False

def deleted_something(type_names, path):
    return True if (type_names[0] in ["IN_MOVED_FROM", "IN_DELETE"]) and not shouldIgnore(path) else False

def store_events(connection, events):
    if events != None:
        normalized_events = []
        for event in events:
            normalized_events.append(( 
                time_parser.convert_to_python_datetime(event[':start']),
                time_parser.convert_to_python_datetime(event[':end']),
                event[':summary']
            ))

            database.store_events(connection, normalized_events)


def call_ics_plugin(connection, file):
    print("PARSING ICS FILE:  ", file)
    return_data = subprocess.run([settings.loaded['ics_parser_bin'], file], stdout=subprocess.PIPE)
    parsed_return = helpers.parse_yaml_string(return_data.stdout.decode('utf8'))
    with connection:
        store_events(connection, parsed_return)
    print("FILE PARSED")

def handle_access(path, filename):
    file = path + '/' + filename

    if filename == 'START':
        print("Starting time monitoring")
        settings.add_runtime('start_timestamp', time.time())

    if os.path.isfile(file):
        file_id = database.store_file(file)


def handle_file_created(connection, path, filename):
    file = path + '/' + filename

    if filename.endswith('.ics'):
        # print("ICS File detected")
        call_ics_plugin(connection, file)

    elif file == (settings.loaded['database'] + '-journal'):
        return

    else:
        file_id = database.store_file(file)


def handle_file_deleted(connection, path, filename):
    file = path + '/' + filename

    if(filename.endswith('.ics')):
        print("File calendar deleted: ", file)
        # callIcsPlugin(file)

    elif file == (settings.loaded['database'] + '-journal'):
        return

    else:
        # print("Deleted file ", file)
        database.delete_file_reference(connection.cursor(), file)
