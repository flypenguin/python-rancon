#!/usr/bin/env python

from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession

import io


VERSION = "0.11.1"

# auto-generate requirements from requirements.txt
install_reqs = parse_requirements("./requirements.txt", session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

long_description = (
    io.open('README.rst', encoding='utf-8').read() +
    '\n' +
    io.open('CHANGES.rst', encoding='utf-8').read()
)

setup(
    name         = 'rancon',
    packages     = find_packages(),
    version      = VERSION,
    description  = 'A python tool which adds Rancher services to Consul based on label selectors',
    author       = 'Axel Bock',
    author_email = 'mr.axel.bock@gmail.com',
    url          = 'https://github.com/flypenguin/python-rancon',
    download_url = 'https://github.com/flypenguin/python-rancon/tarball/{}'.format(VERSION),
    keywords     = ['rancher', 'api', 'consul'],
    install_requires = reqs,
    long_description = long_description,
    entry_points     = {
        'console_scripts': [
            'rancon=rancon:console_entrypoint',
        ],
    },
    classifiers  = [
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Topic :: System :: Systems Administration",
    ],
)
