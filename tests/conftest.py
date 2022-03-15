from pathlib import Path

import pandas as pd
import pytest

from favicon_finder.favicons_runner import FaviconFinder


@pytest.fixture(scope="function")
def get_domains():
    return ["facebook.com", "yahoo.com", "amazon.com"]


@pytest.fixture(scope="function")
def fake_df():
    """Create fake df to output and clean up the resulting csv file."""
    df = pd.DataFrame([["a", "b"], ["c", "d"]], columns=["letter", "domain"])
    results = {"a": 23, "b": 2, "c": 90, "d": 10}
    yield df, results
    path = Path("test_reports/test_csv.csv")
    if path.exists():
        path.unlink()


@pytest.fixture(scope="function")
def small_df():
    df = pd.DataFrame(
        [
            [150, "duckduckgo.com"],
            [553, "wiktionary.org"],
            [28, "myshopify.com"],
            [25, "microsoftonline.com"],
        ],
        columns=["rank", "domain"],
    )
    return df


@pytest.fixture(scope="function")
def setup_finder(small_df):
    finder = FaviconFinder(domain_df=small_df, domains=small_df["domain"].to_list())
    return finder
