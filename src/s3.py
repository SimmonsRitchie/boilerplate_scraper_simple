import logging
import boto3
import os
from definitions import DIR_DATA


def copy_to_s3(file_path, bucket_name, destination_dir):
    logging.info(f"Move {file_path} to s3")

    try:
        # CHECK FILE EXISTS
        if not file_path.is_file():
            logging.error(
                f"No file found at {file_path}," "aborting attempt to move file to S3."
            )
            raise

        # GET ENV VARS
        keyID = os.environ.get("KEY_ID")
        sKeyID = os.environ.get("SECRET_KEY_ID")
        source_path = str(file_path.resolve())
        filename = file_path.name
        destination_path = f"{destination_dir}/{filename}"

        # LOGGING
        logging.info(f"Moving {filename} to S3 bucket {bucket_name}...")
        logging.info(f"File will be saved in: {destination_path}")

        # CONNECT TO S3
        session = boto3.Session(
            aws_access_key_id=keyID,
            aws_secret_access_key=sKeyID,
        )
        s3 = session.resource("s3")

        # UPLOAD
        s3.Bucket(bucket_name).upload_file(
            source_path,
            destination_path,
            ExtraArgs={
                "ACL": "public-read",
                "CacheControl": "proxy-revalidate, max-age=300",
                "ContentType": "text/csv",
                "Metadata": {"Access-Control-Allow-Origin": "*"},
            },
        )

        logging.info(f"file uploaded to {destination_path}")
    except Exception as e:
        logging.error(
            "Something went wrong when attempting to copy file" " to S3 bucket"
        )
        logging.exception(e)
        return
