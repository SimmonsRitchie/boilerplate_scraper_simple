#!/usr/bin/env bash

# Cronjob script - this shell script is intended to be executed by a cronjob to run the program
# at regular intervals. If you're NOT setting up this program to run as a cronjob you can ignore this file and
# simply execute the program as described in the readme.

# If you do wish to set up a cronjob, you can adapt the paths in this script for your own purposes.

# Start
echo "##############################"
echo $(date '+%Y-%m-%d %H:%M:%S')
echo "PROD LOCAL script start"

# This tells pipenv to use this .env file
export PIPENV_DOTENV_LOCATION="./.env"

# Run program
pipenv run python src/run.py
