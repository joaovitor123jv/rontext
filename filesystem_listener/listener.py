import inotify.adapters

def listenPath(path):
    # i = inotify.adapters.InotifyTree(path)
    i = inotify.adapters.Inotify()

    i.add_watch(path)
    
    # for event in i.event_gen():
    for event in i.event_gen(yield_nones = False):
        (_, type_names, path, filename) = event

        if(filename.startswith(".")):
            pass
        else:
            print("PATH=[{}] FILENAME=[{}] EVENT_TYPES=[{}]".format(path, filename, type_names))

def listen(settings):
    listener = inotify.adapters.Inotify()

    for path in settings['listen']:
        print("Adding '", path, "' to listener")
        listener.add_watch(path)

    for event in listener.event_gen(yield_nones = False):
        (_, type_names, path, filename) = event

        if(not filename.startswith('.')):
            if type_names[0] == "IN_MOVED_TO":
                print("Created file, ", filename)
                # print(f"PATH=[{path}] FILENAME=[{filename}] EVENT_TYPES=[{type_names}]")
                if(filename.endswith('.ics')):
                    print("\t\tCALENDAR FILE DETECTED!!! == ", filename)

            elif type_names[0] == "IN_MOVED_FROM":
                print("Deleted file ", filename)

                if(filename.endswith('.ics')):
                    print("\t\tCALENDAR FILE DETECTED!!! == ", filename)
            
            else:
                print("Event type: ", type_names)