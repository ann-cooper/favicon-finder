FROM python:3.9.9-slim

ENV IMAGENAME=favicon_finder

RUN set -ex \
    && apt-get update -y \
    && mkdir /code \
    && mkdir /code/test_reports \
    && groupadd -g 999 appuser \
    && useradd -r -d /code -u 999 -g appuser appuser

WORKDIR /code
COPY . /code

RUN pip install -U pip \
    && pip install -r dev_requirements.txt \
    && chown -R appuser:appuser -R /code \
    && pip install . 

USER appuser

# Test entrypoint
ENTRYPOINT ["python3", "-m", "pytest" ]

# Script entrypoint
# ENTRYPOINT ["python3", "favicon_finder/favicons_runner.py" ]
