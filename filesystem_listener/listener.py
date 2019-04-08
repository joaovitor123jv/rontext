import inotify.adapters
import operations
import settings

def listenPath(path):
    i = inotify.adapters.InotifyTree(path)
    # i = inotify.adapters.Inotify()

    # i.add_watch(path)
    
    # for event in i.event_gen(yield_nones = False):
    for event in i.event_gen():
        (_, type_names, path, filename) = event

        if(filename.startswith(".")):
            pass
        else:
            print("PATH=[{}] FILENAME=[{}] EVENT_TYPES=[{}]".format(path, filename, type_names))

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

        # print(f"PATH=[{path}] FILENAME=[{filename}] EVENT_TYPES=[{type_names}]")
        if(not filename.startswith('.')):
            if operations.createdSomething(type_names):
                operations.handleFileCreated(path, filename)

            elif operations.deletedSomething(type_names):
                operations.handleFileDeleted(path, filename)
            
            else:
                print("Event type: ", type_names)

def listenAll(listener):
    for event in listener.event_gen(yield_nones = False):
        (_, type_names, path, filename) = event

        if operations.createdSomething(type_names):
            operations.handleFileCreated(path, filename)

        elif operations.deletedSomething(type_names):
            operations.handleFileDeleted(path, filename)
        
        else:
            print("Event type: ", type_names)