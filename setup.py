from setuptools import find_packages, setup
import re
from pathlib import Path

def get_reqs():
    path = Path('requirements.txt')
    with open(path, "r") as f:
        text = f.read()
    pattern = re.compile(r'^\w.*?')
    lines = text.split('\n')
    reqs = [line.split("==")[0] for line in lines if re.search(pattern, line)]
    return reqs


setup(
    name="favicon_finder",
    version="1.0.0",
    description="A script for finding favicon links and outputting them to csv",
    author="Ann Cooper",
    author_email="cooperannc@gmail.com",
    packages=find_packages(),
    install_requires=get_reqs(),
    python_requires=">=3.9",
)
