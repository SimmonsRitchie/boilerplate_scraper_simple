import logging
import json
from typing import Dict

import pandas as pd
import pytz

from definitions import PATH_FETCHED_METADATA, PATH_FETCHED_DATA_JSON
from datetime import datetime

from helper.time import convert_utc_to_eastern


def has_json_changed(json_new) -> bool:
    """
    Check if data has changed.

    Args:
        json_new (pd.Dataframe): Fetched data as DataFrame

    Returns:
        bool. True if data has changed.

    """

    # No prior data, immediately return False

    # Return True if new data doesn't match old data
    with open(PATH_FETCHED_DATA_JSON, "r") as fin:
        json_old = json.load(fin)
    return not json_new == json_old


def create_metadata(scrape_time_utc: datetime, df: pd.DataFrame) -> Dict:
    """
    Creates metadata about scrape
    Args:
        scrape_time_utc (datetime):
        df (pd.DataFrame):

    Returns: Dict

    """
    scrape_time_eastern = convert_utc_to_eastern(scrape_time_utc)
    logging.info(
        f"Saving metadata for data scraped on {scrape_time_eastern.strftime('%b %-d %Y, %I:%M %p')}"
    )
    metadata = {
        "scrapeDayOfWeekEastern": scrape_time_eastern.strftime("%A"),
        "scrapeDatetimeIsoEastern": scrape_time_eastern.isoformat(),
        "scrapeDatetimeIsoGMT": scrape_time_utc.astimezone(pytz.utc).isoformat(),
        "scrapeDatetimeUnixGMT": scrape_time_utc.timestamp(),
        "columnNames": df.columns.tolist(),
        "rowCount": len(df.index),
    }
    return metadata
