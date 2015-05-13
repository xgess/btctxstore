#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import os
from setuptools import setup, find_packages


THISDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(THISDIR)


VERSION = open("version.txt").readline().strip()
DOWNLOAD_BASEURL = "https://pypi.python.org/packages/source/a/btctxstore/"
DOWNLOAD_URL = DOWNLOAD_BASEURL + "btctxstore-%s.tar.gz" % VERSION


setup(
    name='btctxstore',
    version=VERSION,
    description=('A simple library to store/retrieve information '
                 'in bitcoin transactions using OP_RETURN.'),
    long_description=open("README.rst").read(),
    keywords=("Bitcoin, OP_RETURN, store, tx, transaction"),
    url='https://github.com/F483/btctxstore/',
    author='Fabian Barkhau',
    author_email='fabian.barkhau@gmail.com',
    license='MIT',
    packages=find_packages(),
    download_url = DOWNLOAD_URL,
    #test_suite="tests",
    install_requires=[
        'apigen == 0.1.6',
        'pycoin == 0.52'
    ],
    tests_require=[ # TODO how to install it?
      'ipython',
      'pudb' # import pudb; pu.db # set break point
      # TODO lint and static analisys
    ],
    zip_safe=False
)

