# import re
from urllib.parse import urlparse
import requests


def url_exists(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False


def uri_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False
