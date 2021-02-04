from slack import send_slack_error_notification


def test_send_slack_error_notification():
    """Test send_slack_error_notification sends message to slack"""
    send_slack_error_notification(
        "Testing slack error notification. This is not a real error. It was sent "
        "intentionally and you can ignore it."
    )
