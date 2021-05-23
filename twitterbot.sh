#!/bin/bash

echo "Starting bot profile $1"
source env/bin/activate
unbuffer python3 main.py $1 2>&1 > "$1.txt"
deactivate
