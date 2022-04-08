#!/usr/bin/env python
# Learn more: https://github.com/kennethreitz/setup.py
import os
from setuptools import setup, find_packages


install_requires = [
    "numpy",
    "pandas",
    "seaborn",
    "matplotlib",
    "leafmap",
    "ipyleaflet",
    "tqdm",
    "geopandas",
    "earthengine-api",
    "eecmip5",
    "joblib",
]

description_file = 'DESCRIPTION.md'
with open(file=description_file, mode='r', encoding='utf-8') as f:
    pypi_description = f.read()

VERSION = open(file='VERSION.txt', mode='r').read().strip()
setup(
    name="climate-resilience",
    version=VERSION,
    description="Download, Preprocessing, and Visualization code for climate resilience data.",
    long_description=pypi_description,
    long_description_content_type="text/markdown",
    author="Satyarth Praveen, Zexuan Xu, Haruko Wainwright",
    author_email="satyarth@lbl.gov, zexuanxu@lbl.gov, hmwainwright@lbl.gov",
    url="https://github.com/ALTEMIS-DOE/climate-resilience.git",
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    # include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    # zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/ALTEMIS-DOE/climate-resilience/issues",
        "Documentation": "https://climate-resilience.readthedocs.io/",
        "Source": "https://github.com/ALTEMIS-DOE/climate-resilience",
    },
)
