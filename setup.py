#!/usr/bin/env python
# Learn more: https://github.com/kennethreitz/setup.py

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

with open(file='README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="climate-resilience",
    version="0.1.8",
    description="Download, Preprocessing, and Visualization code for climate resilience data.",
    long_description=readme,
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
    # package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={"": "src"},
    # include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    # license=about['__license__'],
    # zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # cmdclass={'test': PyTest},
    # tests_require=test_requirements,
    # extras_require={
    #     'security': [],
    #     'socks': ['PySocks>=1.5.6, !=1.5.7'],
    #     'socks:sys_platform == "win32" and python_version == "2.7"': ['win_inet_pton'],
    #     'use_chardet_on_py3': ['chardet>=3.0.2,<5']
    # },
    project_urls={
        "Bug Tracker": "https://github.com/satyarth934/lbnl-climate-resilience/issues",
    #     'Documentation': 'https://requests.readthedocs.io',
        "Source": "https://github.com/satyarth934/lbnl-climate-resilience",
    },
)