#!/usr/bin/env python3

import io
import os
import sys

from setuptools import find_packages, setup

# Package meta-data
NAME = 'dogmon'
LICENSE = 'Apache License 2.0'
DESCRIPTION = 'HTTP log monitoring console program'
URL = 'https://github.com/raphaelh/dogmon'
EMAIL = 'raphael.huck@gmail.com'
AUTHOR = 'Raphaël HUCK'
VERSION = '0.1'
PYTHON_REQUIRES = '>=3.6.0'
INSTALL_REQUIRES = []
EXTRAS_REQUIRES = {'dev': ['pytest', 'flake8', 'wheel']}
SETUP_REQUIRES = []
TESTS_REQUIRES = []

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your
# MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'),
                 encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages('src'),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': ['dogmon=dogmon.main:main'],
    },
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    tests_require=TESTS_REQUIRES,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
