#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Aron Culotta'
__email__ = 'aronwc@gmail.com'
__version__ = '0.1.1'


if bytes == str:  # Python 2.7
    import codecs
    open_read_utf8 = lambda f: codecs.getreader('utf8')(f, 'replace')
    open_write_utf8 = lambda f: codecs.getwriter('utf8')(f, 'replace')
    my_unicode = unicode  # flake8: noqa
else:
    import io
    open_read_utf8 = lambda f: io.TextIOWrapper(f.buffer, 'utf8', 'replace')
    open_write_utf8 = lambda f: io.TextIOWrapper(f.buffer, 'utf8', 'replace')
    my_unicode = str
