import re
from urllib.parse import urlparse
import requests


def is_valid_folder_name(name: str):
    # Define a regular expression pattern to match forbidden characters
    ILLEGAL_NTFS_CHARS = r'[<>:/\\|?*\"]|[\0-\31]'
    # Define a list of forbidden names
    FORBIDDEN_NAMES = ['CON', 'PRN', 'AUX', 'NUL',
                       'COM1', 'COM2', 'COM3', 'COM4', 'COM5',
                       'COM6', 'COM7', 'COM8', 'COM9',
                       'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5',
                       'LPT6', 'LPT7', 'LPT8', 'LPT9']
    # Check for forbidden characters
    match = re.search(ILLEGAL_NTFS_CHARS, name)
    if match:
        return False
    # Check for forbidden names
    if name.upper() in FORBIDDEN_NAMES:
        return False
    # Check for empty name (disallowed in Windows)
    if name.strip() == "":
        return False
    # Check for names starting or ending with dot or space
    match = re.match(r'^[. ]|.*[. ]$', name)
    if match:
        return False
    return True


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
