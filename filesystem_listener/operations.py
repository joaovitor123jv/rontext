import subprocess
import settings
import time_parser
import time
import database
import json
import os


creation_operations = ["IN_MOVED_TO", "IN_CREATE"]
deletion_operations = ["IN_MOVED_FROM", "IN_DELETE"]
close_operations = ['IN_CLOSE_NOWRITE', 'IN_CLOSE_WRITE']

def isProjectRelated(path):
    return bool(
        path.startswith( os.environ['HOME'] + "/Documentos/UFG-CDC/PFC/PFC2/Sistema" )
        or path.startswith( os.environ['HOME'] + "/.ctxt_search-")
    )


def shouldIgnore(path):
    if isProjectRelated(path):
        return True
    for ignored_substring in settings.loaded['ignore_occurrences']:
        if ignored_substring in path:
            return True
    return False


def created_something(type_names, path):
    return (type_names[0] in creation_operations) and not shouldIgnore(path)


def accessed_something(type_names, path):
    print("Accessed: ", type_names, path)
    return (type_names[0] == "IN_OPEN") and not shouldIgnore(path)


def closed_something(type_names, path):
    return (type_names[0] in close_operations) and not shouldIgnore(path)

def deleted_something(type_names, path):
    return (type_names[0] in deletion_operations) and not shouldIgnore(path)


def store_events(connection, events):
    if events != None:
        normalized_events = []
        for event in events:
            normalized_events.append(( 
                time_parser.convert_to_python_datetime(event['start']),
                time_parser.convert_to_python_datetime(event['end']),
                event['summary']
            ))

            database.store_events(connection, normalized_events)


def call_ics_plugin(connection, file):
    print("PARSING ICS FILE:  ", file)
    return_data = subprocess.run([settings.loaded['ics_parser_bin'], file], stdout=subprocess.PIPE)
    parsed_return = json.loads(return_data.stdout.decode('utf8'))
    with connection:
        store_events(connection, parsed_return)
    print("FILE PARSED")

# PARSING ICS FILE:   /home/jovi/Downloads/myevents.ics
# Traceback (most recent call last):
#   File "/home/jovi/code/rontext/filesystem_listener/main.py", line 46, in <module>
#     _main()
#   File "/home/jovi/code/rontext/filesystem_listener/main.py", line 34, in _main
#     listener.listen()
#   File "/home/jovi/code/rontext/filesystem_listener/listener.py", line 28, in listen
#     listenOnlyVisible(connection, listener)
#   File "/home/jovi/code/rontext/filesystem_listener/listener.py", line 39, in listenOnlyVisible
#     operations.handle_file_created(connection, path, filename)
#   File "/home/jovi/code/rontext/filesystem_listener/operations.py", line 77, in handle_file_created
#     call_ics_plugin(connection, file)
#   File "/home/jovi/code/rontext/filesystem_listener/operations.py", line 56, in call_ics_plugin
#     store_events(connection, parsed_return)
#   File "/home/jovi/code/rontext/filesystem_listener/operations.py", line 43, in store_events
#     time_parser.convert_to_python_datetime(event[':start']),
# KeyError: ':start'


def handle_access(path, filename):
    file = path + '/' + filename

    if filename == 'START':
        print("Starting time monitoring")
        settings.add_runtime('start_timestamp', time.time())

    if os.path.isfile(file):
        print("File accessed: ", filename)
        file_id = database.store_file(file)


def handle_file_created(connection, path, filename):
    file = path + '/' + filename

    if filename.endswith('.ics'):
        # print("ICS File detected")
        call_ics_plugin(connection, file)

    elif file == (settings.loaded['database'] + '-journal'):
        return

    else:
        print("File created: ", filename)
        file_id = database.store_file(file)


def handle_file_deleted(connection, path, filename):
    file = path + '/' + filename

    if(filename.endswith('.ics')):
        print("File calendar deleted: ", file)
        # callIcsPlugin(file)

    elif file == (settings.loaded['database'] + '-journal'):
        return

    else:
        print("File deleted: ", filename)
        database.delete_file_reference(connection.cursor(), file)
