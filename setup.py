#!/usr/bin/env python
from setuptools import setup, find_packages
import os

# Define the target directory for the config.yml file
target_directory = os.path.join(os.path.expanduser("~"), ".config", "urless") if os.path.expanduser("~") == os.path.expanduser("~" + os.environ['USER']) else None

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
    data_files=[
        (target_directory, ['config.yml']),
    ],
)
