# Favicon Finder Project

## References

- Gist using BeautifulSoup to look for candidate favicon urls: https://gist.github.com/roma-guru/2f3b57e1a7da9fd9d82daa12cc3a1687
- StackOverflow question about finding favicon urls: https://stackoverflow.com/questions/4674460/how-to-get-favicon-by-using-beautiful-soup-and-python
- Requests docs on using transport adapters: https://docs.python-requests.org/en/latest/user/advanced/#transport-adapters
- Python docs on logging: https://docs.python-guide.org/writing/logging/
- Structured logging formatter: https://github.com/madzak/python-json-logger
- Python docs on multi-threading: https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example

## Setting up a local virtual environment
### With venv
- This project uses 3.9.9
- Create an environment with `python3 -m venv venv`
- Activate it with `source venv/bin/activate`

### With pyenv
- Make sure you have pyenv installed, there is guidance here: https://realpython.com/intro-to-pyenv/
- This project uses python 3.9.9
- Create your pyenv environment with `pyenv virtualenv 3.9.9 favicon_env`
- Activate your environment with `pyenv activate favicon_env`

### Installing requirements
- Install in the activated virtual environment with `pip install -r requirements.txt` or `pip install -r dev_requirements.txt`
- Install the package with `pip install .`

## Managing dependencies
- To update or change dependencies: activate the venv, then install pip-tools with `pip install pip-tools`
- Adjust the packages listed in requirements/main.in as needed.
- To re-output the main.txt: `pip-compile requirements/main.in --output-file=- > requirements.txt`
- To upgrade the packages: `pip-compile requirements.txt`


## Running the script
### In a local virtual environment
- In the activated virtual environment: `python favicon_finder/favicons_runner.py`
### With Docker
- If you want to see the logs as the script runs, uncomment the stream_handler lines in favicon_finder/logger.py (See note in logger.py)

- Use the Docker container: `docker build -t favicon-finder -f Dockerfile .; docker run -it --name favicon-finder-container -t favicon-finder:latest`
- To stop and remove the container: `docker stop favicon-finder-container; docker rm favicon-finder-container`

## Running the tests
### In a local virtual environment
- With an activated virtual environment: `pytest`
### With Docker
- In the Dockerfile, uncomment the test ENTRYPOINT and comment out the script ENTRYPOINT
- Use the Docker container: `docker build -t favicon-finder -f Dockerfile .; docker run -it --name favicon-finder-container -t favicon-finder:latest`
- To stop and remove the container: `docker stop favicon-finder-container; docker rm favicon-finder-container`

------------------

## Original README text

## Prompt

Create an application, that given a CSV file of the first 1000 domains of the [Alexa top million domains][alexa-top-domains], finds their favicon URL, and saves the results to a CSV. The relevant domains can be found in the included file `favicon-finder-top-1k-domains.csv`.

The resulting output CSV, `favicons.csv`, should contain the domain, its Alexa rank, and the full URL path to the favicon in the following structure:

| rank | domain        | favicon_url                                                  |
| ---- | ------------- | ------------------------------------------------------------ |
| 1    | google.com    | https://www.google.com/favicon.ico                           |
| 2    | youtube.com   | https://youtube.com/favicon.ico                              |
| ...  | ...           | ...                                                          |
| 17   | live.com      | https://ow2.res.office365.com/owalanding/2021.8.25.01/images/favicon.ico?v=4 |
| ...  | ...           | ...                                                          |
| 59   | wordpress.com | https://wpcom.files.wordpress.com/2017/11/cropped-wordpress.png?w=16 |
| ...  | ...           | ...                                                          |

(URLs may have changed since time of writing)

Your application should use all reasonable techniques to find the fully qualified domain name and path of the favicon. In the event of errors, they should be included in the output file in a standardised format.

## Deliverable

### Requirements

1. The project processes all 1,000 domains in less than five minutes.
1. The project can be run from the command line.
1. The project contains usage instructions that we can follow to run the project.
1. The project is representative of your own work, though you may use online resources.
    1. If you drew inspiration from any sources in particular, please include a link in your project's README.
1. The project should adhere to best practices of software design.
    1. This might include, but is not limited to, things like: running the project in Docker, writing unit tests, incorporating a linting suite, writing documentation, etc. None of these specific features are required; rather, they are just suggestions based on successful projects we've seen in the past. It's better to finish one of these items than it is to submit several incomplete items.

## Evaluation

When assessing the project, we will be looking for a few things:

1. Does the project meet the requirements of the prompt? **We will not evaluate projects further if they do not meet the prompt requirements**.
1. Can we run the code and reproduce your result? Is the user experience (UX) reasonable?
1. What is the general quality of the code?
1. How is the project organized?

[alexa-top-domains]: https://en.wikipedia.org/wiki/Alexa_Internet#Alexa_Traffic_Rank:~:text=A%20key%20metric%20published%20from%20Alexa,also%20simply%20known%20as%20Alexa%20Rank
