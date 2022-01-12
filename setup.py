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

setup(
    name="climate-resilience",
    version="0.2.3",
    description="Download, Preprocessing, and Visualization code for climate resilience data.",
    long_description=pypi_description,
    long_description_content_type="text/markdown",
    author=[
        "Satyarth Praveen",
        "Zexuan Xu",
    ],
    author_email="satyarth@lbl.gov",
    url="https://github.com/satyarth934/lbnl-climate-resilience",
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
        "Bug Tracker": "https://github.com/satyarth934/lbnl-climate-resilience/issues",
        # 'Documentation': None,
        "Source": "https://github.com/satyarth934/lbnl-climate-resilience",
    },
)