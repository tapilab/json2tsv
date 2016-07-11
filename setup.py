#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='json2tsv',
    version='0.1.1',
    description='Convert json to tab-separated format.',
    long_description=readme + '\n\n' + history,
    author='Aron Culotta',
    author_email='aronwc@gmail.com',
    url='https://github.com/aronwc/json2tsv',
    packages=[
        'json2tsv',
    ],
    package_dir={'json2tsv':
                 'json2tsv'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='json2tsv',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts': [
            'json2tsv = json2tsv.json2tsv:main',
            'tsv2json = json2tsv.tsv2json:main',
        ],
    },
    test_suite='tests',
)
