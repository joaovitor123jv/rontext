import subprocess
import settings
import time_parser
import database
import helpers

# def createdSomething(type_names):
def created_something(type_names):
    return True if (type_names[0] == "IN_MOVED_TO" or type_names[0] == "IN_CREATE") else False

# def deletedSomething(type_names):
def deleted_something(type_names):
    return True if (type_names[0] == "IN_MOVED_FROM" or type_names[0] == "IN_DELETE") else False

def store_events(events):
    if events != None:
        normalized_events = []
        for event in events:
            start_time = time_parser.convert_to_python_datetime(event[':start'])
            end_time = time_parser.convert_to_python_datetime(event[':end'])
            summary = event[':summary']

            normalized_events.append(( start_time, end_time, summary ))

        database.store_events(normalized_events)


def call_ics_plugin(file):
    return_data = subprocess.run([settings.loaded['ics_parser_bin'], file], stdout=subprocess.PIPE)
    parsed_return = helpers.parse_yaml_string(return_data.stdout.decode('utf8'))
    store_events(parsed_return)

# THIS FUNCIONS MUST RETURN RELATIONSHIPS ID IF SOME
# TODO
def detect_relationships(file_id, actual_localization, actual_event):
    pass

# def handleFileCreated(path, filename):
def handle_file_created(path, filename):
    file = path + '/' + filename

    if filename.endswith('.ics'):
        print("CREATE CALENDAR FILE DETECTED!!! == ", file)
        call_ics_plugin(file)

    elif file == (settings.loaded['database'] + '-journal'):
        return

    else:
        print("Created file, ", file)
        file_id = database.store_file(file)
        relationships = detect_relationships(file_id, helpers.get_actual_localization(), helpers.get_actual_event())

# def handleFileDeleted(path, filename):
def handle_file_deleted(path, filename):
    file = path + '/' + filename

    if(filename.endswith('.ics')):
        print("DELETE OF CALENDAR FILE DETECTED!!! == ", file)
        # callIcsPlugin(file)

    elif file == (settings.loaded['database'] + '-journal'):
        return

    else:
        print("Deleted file ", file)
        database.delete_file_reference(file)
