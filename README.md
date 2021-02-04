### Boilerplate Scraper Simple

A simple template for building Python scrapers. Includes support for:

 - Python 3.7
 - Setting up different configurations using .env files.
 - Moving files to S3 using Boto3.
 - Sending slack notifications for errors and/or successful scrapes.
 - A template script for triggering this scraper on an EC2 instance using a cronjob.
 - Archival of past scrapes.
 - Creation of a 'metadata.json' file, to save extraneous info about a scrape, like when it was executed.
 - Logging.
 - Custom exceptions.

Scraped data will be saved in data/output.

#### Install

1. Open the terminal. Clone the project repo.

2. If you don't have pipenv installed on your machine, install it. On Mac, using homebrew, run:

    `brew install pipenv`

3. Navigate into the project directory.
     
4. Use pipenv to create a virtual environment and install the project 
dependencies. Run:

    `pipenv install`

#### Run

To run in local dev mode, navigate into project folder, add a .env.dev file (refer to .env.example for a template) and
 run:

    `pipenv run dev`
    
To run in local production mode, navigate into project folder, add a .env file (refer to .env.example for a template
) file and run:
 
     `pipenv run prod-local`

#### Note

When this project is opened in PyCharm 2019.3 CE, the program may mark imports in src/ as being incorrectly imported. To
 resolve this, right click src/, select 'Mark Directory as', and select 'Sources Root'.