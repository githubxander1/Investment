import logging

import requests

logger = logging.getLogger(__name__)

def send_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise