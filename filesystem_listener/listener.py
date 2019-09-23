import inotify.adapters
import operations
import settings

def listenPath(path):
    i = inotify.adapters.InotifyTree(path)
    for event in i.event_gen():
        (_, type_names, path, filename) = event

        # if not filename.startswith("."):
        #     print("PATH=[{}] FILENAME=[{}] EVENT_TYPES=[{}]".format(path, filename, type_names))

def listen():
    listener = inotify.adapters.Inotify()

    for path in settings.loaded['listen']:
        print("Adding '", path, "' to listener")
        listener.add_watch(path)

    if settings.loaded['ignore_hidden']:
        listenOnlyVisible(listener)

    else:
        listenAll(listener)

def listenOnlyVisible(listener):
    for event in listener.event_gen(yield_nones = False):
        (_, type_names, path, filename) = event

        if not filename.startswith('.') and not filename.startswith('.ctxt_search-'):
            if operations.created_something(type_names):
                operations.handle_file_created(path, filename)

            elif operations.deleted_something(type_names):
                operations.handle_file_deleted(path, filename)

            elif operations.accessed_something(type_names):
                operations.handle_access(path, filename)

            # else:
            #     print("Event type: ", type_names)
            #     print("Filename: ", filename)

def listenAll(listener):
    for event in listener.event_gen(yield_nones = False):
        (_, type_names, path, filename) = event

        if operations.created_something(type_names):
            operations.handle_file_created(path, filename)

        elif operations.deleted_something(type_names):
            operations.handle_file_deleted(path, filename)

        elif operations.accessed_something(type_names):
            operations.handle_access(path, filename)

        # else:
        #     print("Event type: ", type_names)
        #     print("Filename: ", filename)
