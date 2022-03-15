import pandas as pd

from favicon_finder import logger
from favicon_finder.favicons import check_basic_url, check_domains, get_favicon_url
from favicon_finder.pandas_utils import output_csv, read_in_domains

logger = logger.get_logger(__name__)


class FaviconFinder:
    """With a list of domains, checks basic favicon url pattern
    and then searches for favicon links to output a csv of the
    domains and the urls to the favicons or a message if not found.

    Attributes
    ----------
    domain_df: pd.DataFrame
    domains: list
    output_filepath: str, optional
    results: dict
        The collected favicon url info from the basic pattern check
    final_results: dict
        A dictionary created in the last stage with the final updated
        results of the favicon searching.

    Methods
    -------
    _run_first_check()
        Run the threaded checker with the basic favicon url pattern
    _run_second_check_update()
        Run the threaded checker to look for candidate urls for the
        domains not found in the first run and update the results
    _update_not_found()
        Update False and None values to 'not found'
    _log_stats()
        Log not found percentage
    _output_csv()
        Ouput the results to csv
    run
        Run all stages

    Returns
    -------
    final_results: dict
    Outputs csv file
    """

    def __init__(
        self,
        domain_df: pd.DataFrame,
        domains: list,
        output_filepath: str = "favicon_search_results.csv",
    ):
        self.domain_df = domain_df
        self.domains = domains
        self.output_filepath = output_filepath
        self.results = None
        self.final_results = None

    def _run_first_check(self):
        """Run the threaded checker with the basic favicon url pattern"""
        logger.info("Starting first check.")
        self.results = check_domains(domains=self.domains, func=check_basic_url)
        # space: dict of all
        return self.results

    def _run_second_check_update(self):
        """Run the threaded checker to look for candidate urls for the
        domains not found in the first run and update the results"""
        # Find the domains that need to be re-checked
        bad_domains = [k for k, v in self.results.items() if not isinstance(v, str)]
        logger.info(
            f"{len(bad_domains)} domains with favicon links not found in first check."
        )

        second_pass_results = check_domains(domains=bad_domains, func=get_favicon_url)

        # Log out how many domains remain unresolved
        second_pass_bad_domains = {
            k: v for k, v in second_pass_results.items() if not isinstance(v, str)
        }
        logger.info(
            f"{len(second_pass_bad_domains)} domains with favicon links not found in second check."
        )
        self.results.update(second_pass_results)

        return self.results

    def _update_not_found(self):
        """Update False and None values to 'not found'"""
        clean_up = {
            k: "not found" for k, v in self.results.items() if v is None or v is False
        }
        self.results.update(clean_up)
        return self.results

    def _log_stats(self):
        """Log not found percentage"""
        not_found = {
            k
            for k, v in self.results.items()
            if not isinstance(v, str) or v == "not found"
        }
        logger.info(
            f"No favicon url found for {(len(not_found)/1000)*100}% of the domains."
        )
        print(
            f"No favicon url found for {(len(not_found)/1000)*100}% of the domains."
        )

    def _output_csv(self):
        """Ouput the results to csv"""
        output_csv(
            df=self.domain_df, results_dict=self.results, filepath=self.output_filepath
        )
        self.final_results = self.results
        return self.final_results

    def run(self):
        """Run all the above methods sequentially"""
        for stage in [
            self._run_first_check,
            self._run_second_check_update,
            self._update_not_found,
            self._log_stats,
            self._output_csv,
        ]:
            try:
                stage()
                if self.final_results:
                    return self.final_results
            except Exception as e:
                logger.exception(e)


if __name__ == "__main__":  # pragma: no cover
    import time

    start_time = time.time()
    # Get the df and the list of domains and run the script
    domain_df, domains = read_in_domains()
    finder = FaviconFinder(domain_df=domain_df, domains=domains)
    finder.run()
    logger.info(f"Running time: {time.time() - start_time}")
    # Print to screen regardless of whether logger is streaming
    print("Script finished.")
