import concurrent.futures
from typing import Callable, Union

import bs4
import requests

from favicon_finder import logger
from favicon_finder.requests_utils import get_session, icon_info_parser

logger = logger.get_logger(__name__)


def get_favicon_url(
    base_url: str, retries: int = 2, redirects: int = 3, timeout: int = 2
) -> Union[str, bool, tuple]:
    """Use BeautifulSoup to search for candidate favicon urls.

    Args:
        base_url (str): _description_
        retries (int, optional): _description_. Defaults to 0.

    Returns:
        str: URL for the favicon
        bool: False if not found
        tuple: Error args tuple

    Reference:
        https://gist.github.com/roma-guru/2f3b57e1a7da9fd9d82daa12cc3a1687
    """
    full_url = f"http://{base_url}/"
    res = None
    get_session(url=full_url, retries=retries, redirects=redirects)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
    }
    try:
        resp = requests.get(full_url, timeout=timeout, headers=headers)
    except Exception as err:
        logger.error(f"Encountered an error in get_favicon_url: {err}")
        return err.args
    else:
        page = bs4.BeautifulSoup(resp.text, "html.parser")
        links = page.find_all(name="link")
        if links:
            res = icon_info_parser(links=links, base_url=base_url)
        elif resp.status_code != 200:
            res = resp.status_code
        else:
            res = (resp.status_code, "link not found")
        return res if res else False


def check_basic_url(url: str) -> Union[str, bool]:
    """Return URL for the most common favicon location
    if found, else False.

    Args:
        url (str): The domain to check

    Returns:
        Union[str, bool]: The favicon URL or False
    """
    full_url = f"http://{url}/favicon.ico"
    get_session(url=full_url, retries=0, redirects=3)
    try:
        code = requests.get(full_url, timeout=2).status_code
    except Exception as err:
        logger.error(f"Exception encountered in check_basic_url: {err}")
        return err.args
    else:
        if code == 200:
            return full_url


def check_domains(domains: list, func: Callable) -> dict:
    """Use threading to look for favicons in common location or
    search for candidate links and return a dictionary of the results.

    Args:
        domains (list): List of domains to check.

    Returns:
        dict: {domain: url or result}

    Reference:
        https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example
    """
    results_dict = {}
    logger.info("Starting favicon link search.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        check_domain = {executor.submit(func, domain): domain for domain in domains}
        for future in concurrent.futures.as_completed(check_domain):
            full_favicon_url = False
            url = check_domain[future]
            try:
                full_favicon_url = future.result()
            except Exception as exc:
                logger.warning(f"Exception encountered for {url}: {exc}")
                full_favicon_url = exc.args
            else:
                results_dict[url] = full_favicon_url

    return results_dict
