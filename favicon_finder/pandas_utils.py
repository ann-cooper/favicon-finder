import pandas as pd

from favicon_finder import logger

logger = logger.get_logger(__name__)


def read_in_domains() -> tuple:
    """Read in list of domains to check.

    Returns:
        tuple: A DataFrame of the domains and ranking, the domains to check
    """
    logger.info("Reading in domains to check.")
    domain_df = pd.read_csv(
        "favicon-finder-top-1k-domains.csv", names=["rank", "domain"]
    )
    domains = domain_df["domain"].to_list()
    return domain_df, domains


def output_csv(
    df: pd.DataFrame, results_dict: dict, filepath: str = "favicon_search_results.csv"
):
    """Write out csv of the favicon search results.

    Args:
        results_dict (dict): Dictionary with the domain as
        key and the result as value
    """
    logger.info("Writing out csv.")
    df["favicon_url"] = df["domain"].map(results_dict)

    df.to_csv(filepath)
