import requests
import json
import logging
import os

from exceptions import NoEnvVarError


def send_slack_error_notification(error_msg: str) -> None:
    message = (
        f"{' '.join([':exclamation:' for _ in range(1, 10)])}\n\n"
        "*ERROR:* COVID vax provider scraper encountered an error:\n\n"
        f"_{error_msg}_"
    )
    send_slack_notification(message)


def send_slack_notification(message: str) -> None:
    slack_webhooks_url = os.getenv("SLACK_WEBHOOKS_URL")
    if not slack_webhooks_url:
        raise NoEnvVarError("SLACK_WEBHOOKS_URL")
    logging.info(f"Sending Slack payload to: {slack_webhooks_url}")
    block = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": message},
        }
    ]
    payload = {"blocks": block}
    payload_json = json.dumps(payload)
    response = requests.post(slack_webhooks_url, data={"payload": payload_json})
    response.raise_for_status()
