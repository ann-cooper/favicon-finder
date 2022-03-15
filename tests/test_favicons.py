import pytest

from favicon_finder.favicons import check_basic_url, check_domains, get_favicon_url
from tests import params


@pytest.mark.parametrize(
    "id, func, expected", params.check_domain_params, ids=params.check_domain_ids
)
def test_check_domains(get_domains, id, func, expected):

    results = check_domains(domains=get_domains, func=func)

    assert results == expected


def test_check_url_exception(caplog):

    results = check_domains(domains=["washingtonpost.com"], func=check_basic_url)
    actual = [rec.message for rec in caplog.records]

    assert isinstance(results["washingtonpost.com"], tuple)
    assert "Read timed out." in " ".join(actual)


@pytest.mark.parametrize(
    "id, domain, expected", params.get_fav_url_params, ids=params.get_fav_url_ids
)
def test_get_favicon_url(id, domain, expected):
    result = get_favicon_url(base_url=domain)

    assert result == expected


def test_get_favicon_url_exception(caplog):
    result = get_favicon_url(base_url="microsoftonline.com")
    logs = " ".join([rec.message for rec in caplog.records])

    assert "Encountered an error in get_favicon_url" in logs
    assert isinstance(result, tuple)
