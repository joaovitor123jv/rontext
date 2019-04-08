#!/usr/bin/env python3

import os
import sys
import config_file_handler

import listener

def _main():
    if(len(sys.argv) == 2):
        print("Argument == ", sys.argv[1])

        if(os.path.isdir(sys.argv[1])):
            print("Argument is a directory, i'll start listening there so")
            listener.listenPath(sys.argv[1])

        else:
            print("This directory doesnt exists")

    else:
        settings = config_file_handler.parseConfigFile()
        print("Loaded settings = ", settings)
        listener.listen()

if __name__ == '__main__':
    _main()