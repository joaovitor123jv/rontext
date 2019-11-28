import inotify.adapters
import operations
import settings
import database

import time

inicio = None

def listen():
    listener = None
    if settings.loaded['recursive_listening']:
        # print("LOG: Enabling recursive listening in ", settings.loaded['listen'][0])
        try:
            listener = inotify.adapters.InotifyTree(settings.loaded['listen'][0])
            print("LOG: listener created")
        except PermissionError:
            print("FAILED to add one directory to listening")

    else:
        listener = inotify.adapters.Inotify()
        for path in settings.loaded['listen']:
            # print("Adding '", path, "' to listener")
            listener.add_watch(path)

    connection = database.connect()
    if settings.loaded['ignore_hidden']:
        listenOnlyVisible(connection, listener)

    else:
        listenAll(connection, listener)

def listenOnlyVisible(connection, listener):
    for event in listener.event_gen(yield_nones = False):
        (_, type_names, path, filename) = event
        if not filename.startswith('.'):
            if operations.created_something(type_names, path):
                operations.handle_file_created(connection, path, filename)
            elif operations.deleted_something(type_names, path):
                operations.handle_file_deleted(connection, path, filename)
            elif operations.accessed_something(type_names, path):
                operations.handle_access(path, filename)

def listenAll(connection, listener):
    for event in listener.event_gen(yield_nones = False):
        (_, type_names, path, filename) = event
        if operations.created_something(type_names, path):
            operations.handle_file_created(connection, path, filename)
        elif operations.deleted_something(type_names, path):
            operations.handle_file_deleted(connection, path, filename)
        elif operations.accessed_something(type_names, path):
            operations.handle_access(path, filename)

