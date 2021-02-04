#!/usr/bin/env bash

# Start
echo "##############################"
echo $(date '+%Y-%m-%d %H:%M:%S')
echo "DEV script start"

# This tells pipenv to use this .env file
export PIPENV_DOTENV_LOCATION="./.dev.env"

# Run program
pipenv run python src/run.py
