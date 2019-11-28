#!/usr/bin/env python3

# Made to run with Python 3.7.x

import os
import sys
import config_file_handler

import settings
import database
import listener
import localization

import threading

def start_file_insert_handler():
    try:
        print("Starting file insert handler")
        thread = threading.Thread(target=database.file_insert_handler)
        thread.start()
        print("File insert handler started")
    except:
        print("Failed to start file insert handler")

def _main():
    print("**** MAIN_THREAD ID == ", threading.get_ident())
    loaded_settings = config_file_handler.parseConfigFile()
    print("Loaded settings = ", loaded_settings)
    database.setup_schema()
    if loaded_settings['use_localization']:
        localization.start_plugin()

    start_file_insert_handler()

    listener.listen()

def cleanup():
    exit(0)

import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    _main()
