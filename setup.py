#!/usr/bin/env python
import os
import shutil
from setuptools import setup, find_packages

# Define the target directory for the config.yml file
target_directory = os.path.join(os.path.expanduser("~"), ".config", "urless") if os.path.expanduser("~") == os.path.expanduser("~" + os.environ['USER']) else None

# Copy the config.yml file to the target directory if it exists
if target_directory and os.path.isfile("config.yml"):
    os.makedirs(target_directory, exist_ok=True)
    shutil.copy("config.yml", target_directory)

setup(
    name="urless",
    packages=find_packages(),
    version=__import__('urless').__version__,
    description="De-clutter a list of URLs",
    long_description=open("README.md").read(),
    author="@xnl-h4ck3r",
    url="https://github.com/xnl-h4ck3r/urless",
    zip_safe=False,
    install_requires=["argparse", "pyyaml", "termcolor", "urlparse3"],
    entry_points={
        'console_scripts': [
            'urless = urless.urless:main',
        ],
    },
)
