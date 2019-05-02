#!/usr/bin/env python3

# Made to run with Python 3.6.7

import os
import sys
import config_file_handler

import settings
import database
import listener
import localization

def _main():
    if(len(sys.argv) == 2):
        print("Argument == ", sys.argv[1])

        if(os.path.isdir(sys.argv[1])):
            print("Argument is a directory, i'll start listening there so")
            listener.listenPath(sys.argv[1])

        else:
            print("This directory doesnt exists")

    else:
        loaded_settings = config_file_handler.parseConfigFile()
        print("Loaded settings = ", loaded_settings)
        database.connect()
        database.setup_schema()
        if settings.loaded['use_localization']:
            localization.start_plugin

        listener.listen()

def cleanup():
    database.close()
    exit(0)

import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    _main()