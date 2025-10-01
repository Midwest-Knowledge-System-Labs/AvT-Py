#!/usr/bin/env python3
"""
A setuptools based setup module.

To learn more about distributing python packages, see:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
https://realpython.com/python-wheels/  # more info on packaging dynamic libraries here
https://stackoverflow.com/questions/31380578/how-to-avoid-building-c-library-with-my-python-package
https://packaging.python.org/en/latest/overview/

https://blog.ian.stapletoncordas.co/2019/02/distributing-python-libraries-with-type-annotations.html
"""

from setuptools import setup

setup(
    name="AvesTerra",
    version="25.01.2",
    description="Python Avial Library",
    author="Midwest Knowledge System Labs",
    author_email="avesterra@georgetown.edu ; dev@midwksl.net ; dev@ledr.io",
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "License :: Proprietary License",
        "Development Status :: Beta",
    ],
    python_requires=">=3.10",
    install_requires=["tabulate"],
    include_package_data=True,
    package_dir={
        "": "src",
    },
    packages=["avesterra", "orchestra", "midwksl", "machinations"],
    package_data={
        "avesterra": ["py.typed"],
        "orchestra": ["py.typed"],
        "midwksl": ["py.typed"],
        "machinations": ["py.typed"]
    },

)