import requests
import logging
from pprint import pprint
from typing import List, Dict, Any

from exceptions import NoJsonDataError
from helper.misc import env_bool
from slack import send_slack_error_notification

BASE_URL = "https://services1.arcgis.com/Nifc7wlHaBPig3Q3/arcgis/rest/services/Vaccine_Provider_Information/FeatureServer/0/query"
PAYLOAD = {
    "f": "json",
    "spatialRel": "esriSpatialRelIntersects",
    "where": "1=1",
    "outfields": "*",
    "returnGeometry": "false",
    "orderByFields": "objectid asc",
    "resultOffset": 0,
    "resultRecordCount": 5000,
}


def fetch_vax_providers() -> List[Dict[str, Any]]:
    """
    Fetch Pa. DoH covid provider data using Arc API.

    Returns:  List[Dict[str, Any]]

    """
    logging.info(f"Getting data at: {BASE_URL}...")
    r = requests.get(BASE_URL, params=PAYLOAD)
    logging.info("Data fetched. Parsing data...")
    json = r.json()
    if not json:
        raise NoJsonDataError
    data = json["features"]

    clean_data = []
    for datum in data:
        clean_data.append({**datum["attributes"]})
    logging.info("Data parsed.")
    return clean_data
