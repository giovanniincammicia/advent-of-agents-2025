import logging

from google.cloud import logging as google_cloud_logging


def setup_logging() -> google_cloud_logging.Logger:
    """Set up logging with basic config and Google Cloud Logging client."""
    logging.basicConfig(level=logging.INFO)
    logging_client = google_cloud_logging.Client()
    logger = logging_client.logger(__name__)
    return logger