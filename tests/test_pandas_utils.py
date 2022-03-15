from pathlib import Path

import pandas as pd

from favicon_finder.pandas_utils import output_csv, read_in_domains


def test_read_in_domains():
    df, domains = read_in_domains()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1000
    assert isinstance(domains, list)
    assert len(domains) == 1000


def test_ouput_csv(fake_df):
    df, results = fake_df
    output_csv(df=df, results_dict=results, filepath="test_reports/test_csv.csv")
    assert Path("test_reports/test_csv.csv").exists()
