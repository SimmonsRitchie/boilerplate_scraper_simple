import json
import logging
import os
import pandas as pd
from definitions import PATH_FETCHED_DATA_CSV, DIR_DATA_ARCHIVE
from exceptions import NoEnvVarError
from helper.init_program import init_program
from helper.misc import env_bool, get_files_in_dir, remove_oldest_files
from helper.time import utc_now, format_datetime_eastern, convert_utc_to_eastern
from s3 import copy_to_s3
from scrape import fetch_data
from process import has_json_changed, create_metadata
from slack import send_slack_notification, send_slack_error_notification
from definitions import PATH_FETCHED_DATA_JSON, DIR_DATA_OUTPUT, PATH_FETCHED_METADATA
from shutil import copyfile


def main():

    # INIT
    init_program()

    # GET ENVS
    enable_s3 = env_bool("ENABLE_S3")
    enable_slack = env_bool("ENABLE_SLACK")
    enable_archive = env_bool("ENABLE_ARCHIVE")
    bucket_name = os.getenv("BUCKET_NAME")
    destination_dir = os.getenv("BUCKET_DESTINATION_DIR")

    # FETCH
    json_new = fetch_data()
    scrape_time_utc = utc_now()

    # CHECK: prior data exists
    if not PATH_FETCHED_DATA_JSON.exists():
        logging.info(f"No prior data, data will be saved for first time...")
    else:
        # CHECK: prior data exists, so compare to see if it is different from old
        if not has_json_changed(json_new):
            logging.info("No change to data, ending program run.")
            return
        # CHECK: new data is not None empty string
        else:
            logging.info(
                f"Data doesn't match prior data, new data will overwrite old..."
            )

    # SAVE - json, CSV, metadata
    logging.info(f"Saving json at: {PATH_FETCHED_DATA_JSON}")
    with open(PATH_FETCHED_DATA_JSON, "w") as fout:
        json.dump(json_new, fout)
    df_new = pd.DataFrame(json_new)
    df_new.to_csv(PATH_FETCHED_DATA_CSV, index=False)
    logging.info(f"Saving csv at: {PATH_FETCHED_DATA_CSV}")
    metadata = create_metadata(scrape_time_utc, df_new)
    with open(PATH_FETCHED_METADATA, "w") as fout:
        json.dump(metadata, fout)

    # ARCHIVE
    if enable_archive:
        logging.info("ENABLE_ARCHIVE env var is set. Archiving data...")
        DIR_DATA_ARCHIVE.mkdir(parents=True, exist_ok=True)
        scrape_datetime_eastern = convert_utc_to_eastern(scrape_time_utc).strftime(
            "%Y-%m-%d--%X"
        )
        filename_csv_archive = (
            f"{scrape_datetime_eastern}__{PATH_FETCHED_DATA_CSV.name}"
        )
        path_csv_archive = DIR_DATA_ARCHIVE / filename_csv_archive
        copyfile(PATH_FETCHED_DATA_CSV, path_csv_archive)
        logging.info("Data archived")
        remove_oldest_files(DIR_DATA_ARCHIVE, 5)
    else:
        logging.info(
            "ENABLE_ARCHIVE env_var is disabled. Scraped data will not be archived."
        )

    # MOVE TO S3
    if enable_s3:
        if not bucket_name:
            raise NoEnvVarError("BUCKET_NAME")
        if not destination_dir:
            raise NoEnvVarError("BUCKET_DESTINATION_DIR")
        files = get_files_in_dir(DIR_DATA_OUTPUT)
        for file in files:
            copy_to_s3(file, bucket_name, destination_dir)
    else:
        logging.info(
            "ENABLE_S3 env var is not set to TRUE. Files will not be moved to s3."
        )

    # SEND SLACK NOTIFICATION
    if enable_slack:
        csv_url = (
            f"https://{bucket_name}/{destination_dir}/{PATH_FETCHED_DATA_CSV.name}"
        )
        json_url = (
            f"https://{bucket_name}/{destination_dir}/{PATH_FETCHED_DATA_JSON.name}"
        )
        meta_url = (
            f"https://{bucket_name}/{destination_dir}/{PATH_FETCHED_METADATA.name}"
        )
        msg = (
            f"{' '.join([':syringe:' for _ in range(1, 10)])}\n\n"
            f"*UPDATE:* New Pa. vaccine provider data appears to be available:\n\n"
            f"List of {metadata['rowCount']} providers has been uploaded here:\n\n"
            f"CSV: {csv_url}\n\n"
            f"JSON: {json_url}\n\n"
            f"metadata: {meta_url}\n\n"
            f":clock3: Data fetched: {format_datetime_eastern(scrape_time_utc)} Eastern"
        )
        send_slack_notification(msg)
    else:
        logging.info(
            "ENABLE_SLACK env var is not set to TRUE. No slack notification will be sent."
        )

    logging.info("Program run complete")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        logging.error(err)
        enable_slack = env_bool("ENABLE_SLACK")
        if enable_slack:
            logging.info("Slack notifications are enabled. Sending error message...")
            send_slack_error_notification(err)
        else:
            logging.info(
                "Slack notifications are disabled. No error message will be sent."
            )
