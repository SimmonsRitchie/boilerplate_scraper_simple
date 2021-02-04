#!/usr/bin/env bash

# Cronjob script - this script is intended to be executed by a cronjob to run this program on an EC2 instance
# at regular intervals.

# Start
echo "##############################"
echo $(date '+%Y-%m-%d %H:%M:%S')
echo "PROD EC2 script start"
# This tells pipenv to use this .env file
export PIPENV_DOTENV_LOCATION="/home/dansr/projects/scraper_pa_vax_providers/.env"
# Navigate to scraper project directory
cd /home/dansr/projects/scraper_pa_vax_providers/
# Run program
# Note: In this case executing path to binary due to problems with pyenv working in cron
~/.pyenv/versions/3.6.10/bin/pipenv run python src/run.py
echo "Script end"