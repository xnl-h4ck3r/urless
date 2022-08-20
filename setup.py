#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="urless",
    packages=find_packages(),
    version="0.1",
    description="De-clutter a list of URLs",
    long_description=open("README.md").read(),
    author="@xnl-h4ck3r",
    url="https://github.com/xnl-h4ck3r/urless",
    py_modules=["urless"],
    install_requires=["argparse","pyyaml","termcolor","urlparse3"],
)
