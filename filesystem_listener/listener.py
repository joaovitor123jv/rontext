import inotify.adapters
import sys
import os

def listen(path):
    i = inotify.adapters.InotifyTree(path)

    # i.add_watch(path)

    # with open('/tmp/test_file', 'w'):
    #     pass
    
    # for event in i.event_gen(yield_nones = False):
    for event in i.event_gen():
        (_, type_names, path, filename) = event

        if(filename.startswith(".")):
            pass
        else:
            print("PATH=[{}] FILENAME=[{}] EVENT_TYPES=[{}]".format(path, filename, type_names))


def _main():
    if(len(sys.argv) == 2):
        print("Argument == ", sys.argv[1])

        if(os.path.isdir(sys.argv[1])):
            print("Argument is a directory, i'll start listening there so")
            listen(sys.argv[1])

        else:
            print("This directory doesnt exists")

    else:
        print("I'll listen in default directory, that is: ", os.environ['HOME'])
        listen(os.environ['HOME'])


if __name__ == '__main__':
    _main()