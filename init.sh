#!/bin/bash

./filesystem_listener/main.py &

sleep 3

disown -h 1

./virtual_filesystem/main.py &

sleep 3
disown -h 1
