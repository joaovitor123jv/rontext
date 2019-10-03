#!/usr/bin/env python3

# Made to run with Python 3.6.7

import os
import sys
import config_file_handler

import settings
import database
import listener
import localization


import threading

def _main():
    print("**** MAIN_THREAD ID == ", threading.get_ident())
    loaded_settings = config_file_handler.parseConfigFile()
    print("Loaded settings = ", loaded_settings)
    database.connect()
    database.setup_schema()
    if loaded_settings['use_localization']:
        localization.start_plugin()

    listener.listen()

def cleanup():
    database.close()
    exit(0)

import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    _main()
