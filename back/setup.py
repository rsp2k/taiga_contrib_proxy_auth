#!/usr/bin/env python
# -*- coding: utf-8 -*-

import versiontools_support
from setuptools import setup, find_packages

setup(
    name = 'taiga-contrib-proxy-auth',
    version = ":versiontools:taiga_contrib_proxy_auth:",
    description = "The Taiga plugin for proxy authentication",
    long_description = "",
    keywords = 'taiga, proxy, auth, plugin',
    author = 'Rupesh Kumar',
    url = 'https://github.com/rupeshk',
    license = 'AGPL',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[],
    setup_requires = [
        'versiontools >= 1.9',
    ],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
