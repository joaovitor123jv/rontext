import inotify.adapters
import operations
import settings

def listen():
    listener = None
    if settings.loaded['recursive_listening']:
        print("LOG: Enabling recursive listening in ", settings.loaded['listen'][0])
        try:
            listener = inotify.adapters.InotifyTree(settings.loaded['listen'][0])
        except PermissionError:
            print("FAILED to add one directory to listening")

    else:
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
                print(f"ONLY VISIBLE Type names == {type_names}")
                operations.handle_access(path, filename)

def listenAll(listener):
    for event in listener.event_gen(yield_nones = False):
        (_, type_names, path, filename) = event

        if operations.created_something(type_names):
            operations.handle_file_created(path, filename)

        elif operations.deleted_something(type_names):
            operations.handle_file_deleted(path, filename)

        elif operations.accessed_something(type_names):
            print(f"LISTEN ALL Type names == {type_names}")
            operations.handle_access(path, filename)

        # else:
        #     print("Event type: ", type_names)
        #     print("Filename: ", filename)
