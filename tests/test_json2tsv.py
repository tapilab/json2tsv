#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_json2tsv
----------------------------------

Tests for `json2tsv` module.
"""
import io
import json

from json2tsv import json2tsv


def test_basic_call():
    input = io.StringIO(
        json.dumps({'foo': 1, 'bar': {'baz': "stuff"}}) + "\n" +
        json.dumps({'foo': 2, 'bar': {'baz': None}}) + "\n" +
        json.dumps({'foo': 3, 'bar': {'baz': "stuff"}}) + "\n" +
        json.dumps({'foo': 4}) + "\n" +
        json.dumps({'foo': 5, 'bar': [1, 2, 3]}) + "\n" +
        json.dumps({'foo': 6, 'bar': {'baz': "stuff"}}) + "\n")
    output = io.StringIO()
    fields = ["foo", "bar.baz"]
    headers = True
    json2tsv.run(input, output, fields, headers)
    output.seek(0)
    assert output.read() == \
        "foo\tbar.baz\n" + \
        "1\tstuff\n" + \
        "2\tnull\n" + \
        "3\tstuff\n" + \
        "4\tnull\n" + \
        "5\tnull\n" + \
        "6\tstuff\n"
