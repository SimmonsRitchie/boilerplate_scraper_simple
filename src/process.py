import logging
import json
from typing import Dict, List, Any

import pandas as pd
import pytz

from definitions import PATH_FETCHED_METADATA, PATH_FETCHED_DATA_JSON, PATH_FETCHED_DATA_CSV
from datetime import datetime

from helper.time import convert_utc_to_eastern


def has_json_changed(json_new: List[Dict[str, Any]]) -> bool:
    """
    Check if data has changed.

    Args:
        json_new (List[Dict[str, Any]]): Fetched data

    Returns:
        bool. True if data has changed.

    """
    # Return True if new data doesn't match old data
    with open(PATH_FETCHED_DATA_JSON, "r") as fin:
        json_old = json.load(fin)
    return not json_new == json_old


def has_csv_changed(df_new: pd.DataFrame) -> bool:
    """
    Check if CSV data, provided as a Pandas DataFrame, has the same shape and values
     as another CSV loaded as a Pandas Dataframe.

    Args:
        df_new (pd.Dataframe): CSV in DataFrame fprm

    Returns:
        bool. True if data is different than .

    """

    df_old = pd.read_csv(PATH_FETCHED_DATA_CSV)
    matches = df_old.equals(df_new)
    return not matches


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
