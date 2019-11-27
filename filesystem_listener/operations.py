import subprocess
import settings
import time_parser
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
    store_events(connection, parsed_return)
    print("FILE PARSED")

def get_relationships(connection, file_id):
    event_summary = None
    event = None
    relationships = None

    if settings.loaded['use_agenda']:
        event = helpers.get_actual_event(connection)


    event = event[1] if event != None else "NULL"
    # if event != None:
    #     event_summary = event[1]
    # else:
    #     event_summary = "NULL"

    if settings.loaded['use_localization'] and settings.loaded['use_agenda']:
        relationships = {
            'file_id': file_id,
            'localization_id': helpers.get_actual_localization(connection),
            'event_summary': event_summary
        }
    elif settings.loaded['use_localization']:
        relationships = {
            'file_id': file_id,
            'localization_id': helpers.get_actual_localization(connection),
            'event_summary': None
        }

    elif settings.loaded['use_agenda']:
        relationships = {
            'file_id': file_id,
            'localization_id': None,
            'event_summary': event_summary
        }

    else:
        relationships = {
            'file_id': file_id,
            'localization_id': None,
            'event_summary': None
        }

    return relationships

def handle_access(connection, path, filename):
    file = path + '/' + filename

    if os.path.isfile(file):
        # print("Arquivo aberto == ", file)
        file_id = database.store_file(connection, file, 1)
        database.increase_file_hits(connection, file)
        relationships = get_relationships(connection, file_id)
        database.store_relationship(connection, relationships)


def handle_file_created(connection, path, filename):
    file = path + '/' + filename

    if filename.endswith('.ics'):
        # print("ICS File detected")
        call_ics_plugin(connection, file)

    elif file == (settings.loaded['database'] + '-journal'):
        return

    else:
        file_id = database.store_file(connection, file, 1)
        relationships = get_relationships(connection, file_id)
        database.store_relationship(connection, relationships)


def handle_file_deleted(connection, path, filename):
    file = path + '/' + filename

    if(filename.endswith('.ics')):
        print("File calendar deleted: ", file)
        # callIcsPlugin(file)

    elif file == (settings.loaded['database'] + '-journal'):
        return

    else:
        # print("Deleted file ", file)
        database.delete_file_reference(connection, file)
