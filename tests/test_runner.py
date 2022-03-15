from unittest import mock

from favicon_finder.favicons_runner import FaviconFinder


def test_runner_with_sample_domains(setup_finder):
    results = setup_finder.run()

    assert len(results) == 4
    assert len([k for k, v in results.items() if isinstance(v, str)]) == 3


def test_all_stages_called(setup_finder):
    """Pass mocked instanced of FaviconsFinder and record calls to show that all methods were called"""

    mock_finder = mock.MagicMock(FaviconFinder, autospec=True)
    mock_finder.final_results = None
    FaviconFinder.run(mock_finder)

    mock_finder._run_first_check.assert_called_once()
    mock_finder._run_second_check_update.assert_called_once()
    mock_finder._update_not_found.assert_called_once()
    mock_finder._log_stats.assert_called_once()
    mock_finder._output_csv.assert_called_once()
