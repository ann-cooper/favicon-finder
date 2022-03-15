from urllib.parse import urlparse, urlunparse

import requests

from favicon_finder import logger

logger = logger.get_logger(__name__)


def get_session(url: str, retries: int, redirects: int) -> requests.Session:
    """Return a request session with limited retries.

    Args:
        url (str): URL to create request session for
        retries (int): number of times to retry

    Returns:
        _type_: requests.Session

    Reference:
        https://docs.python-requests.org/en/latest/user/advanced/#transport-adapters
    """
    session = requests.Session()
    session.max_redirects = redirects
    session.mount(url, requests.adapters.HTTPAdapter(max_retries=retries))

    return session


def icon_info_parser(links: list, base_url: str) -> str:
    """Given a list of candidate links, return the link to the favicon.

    Args:
        links (list): List of links found in the page
        base_url (str): The domain

    Returns:
        str: Favicon url
    """
    icons = [url for url in links if "icon" in url.attrs.get("rel", "not found")]
    if icons:
        result = icons[0].attrs.get("href")
        url = urlparse(result, scheme="http")
        if not url.netloc:
            result = urlunparse((url.scheme, base_url, url.path, "", "", ""))
        return result
