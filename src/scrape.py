import requests
import logging
from pprint import pprint
from typing import List, Dict, Any

from exceptions import NoJsonDataError
from helper.misc import env_bool
from slack import send_slack_error_notification

BASE_URL = "https://jsonplaceholder.typicode.com/comments"
QUERY_PARAMS = {
    "postId": 1
}


def fetch_data() -> List[Dict[str, Any]]:
    """
    Request data from a server, return JSON-like data.

    Returns:  List[Dict[str, Any]]

    """
    logging.info(f"Getting data at: {BASE_URL}...")
    r = requests.get(BASE_URL, params=QUERY_PARAMS)
    logging.info("Data fetched. Parsing data...")
    json = r.json()
    if not json:
        raise NoJsonDataError
    return json
