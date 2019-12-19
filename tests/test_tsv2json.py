#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_json2tsv
----------------------------------

Tests for `json2tsv` module.
"""
import io
import json

from json2tsv import tsv2json


def test_basic_call():
    input = io.StringIO(
        "foo\tbar.baz\n" +
        "1\tstuff\n" +
        "2\tnull\n" +
        "3\tstuff\n" +
        "4\tnull\n" +
        "5\tnull\n" +
        "6\tstuff\n")
    output = io.StringIO()
    type_strs = ["int", "str"]
    null_str = "null"
    tsv2json.run(input, output, type_strs, null_str)
    output.seek(0)
    output_json = [json.loads(line) for line in output]
    print(output_json)
    assert output_json == \
        [{'foo': 1, 'bar': {'baz': "stuff"}},
         {'foo': 2, 'bar': {'baz': None}},
         {'foo': 3, 'bar': {'baz': "stuff"}},
         {'foo': 4, 'bar': {'baz': None}},
         {'foo': 5, 'bar': {'baz': None}},
         {'foo': 6, 'bar': {'baz': "stuff"}}]
