"""
This file contains important project variables.
"""
import os
from pathlib import Path

# This sets our root directory as the project directory
ROOT_DIR = (
    Path(os.path.dirname(os.path.abspath(__file__))) / ".."
)  # This is your Project Root

# DIRECTORIES
DIR_DATA = ROOT_DIR / "data"
DIR_SRC = ROOT_DIR / "src"
DIR_TESTS = ROOT_DIR / "tests"
DIR_INPUT = DIR_DATA / "input"
DIR_LOGS_OUTPUT = DIR_DATA / "logs"
DIR_LOGS_CONFIG = DIR_SRC / "logs_setup/config"
DIR_DATA_OUTPUT = DIR_DATA / "output"
DIR_DATA_ARCHIVE = DIR_DATA / "archive"
DIR_TESTS_FIXTURES = DIR_TESTS / "fixtures"


# PATHS
PATH_LOGS_CONFIG = DIR_LOGS_CONFIG / "logging.yaml"
PATH_LOGS_CONFIG_TEST = DIR_LOGS_CONFIG / "logging_test.yaml"
PATH_FETCHED_DATA_JSON = DIR_DATA_OUTPUT / "data.json"
PATH_FETCHED_DATA_CSV = DIR_DATA_OUTPUT / "data.csv"
PATH_FETCHED_METADATA = DIR_DATA_OUTPUT / "metadata.json"
