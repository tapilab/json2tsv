#!/usr/bin/env python
"""
Convert tsv to json from stdin, assuming first line is header.


e.g., cat my.tsv | json2tsv int str bool
"""
import argparse
import json
import sys
import traceback

from . import util

TYPES = {
    'str': lambda v: v,
    'int': int,
    'float': float,
    'bool': lambda v: v.lower() in ("true", "t", "1", "y"),
    'json': json.loads
}


def main():
    parser = argparse.ArgumentParser(
        description='Convert tsv to json from stdin, assuming first line is ' +
                    'header.')
    parser.add_argument(
        'type', nargs='*',
        help='The types of column values in the order they appear in ' +
             'the file.  If left unspecified, all columns will be ' +
             'assumed to be `str`.  Possible types are `str`, `int`, ' +
             '`float`, `bool`, or `json`.')
    parser.add_argument('--null-str', default="null", help='fields to print')
    args = parser.parse_args()

    input = util.read(sys.stdin)
    output = util.write(sys.stdout)

    run(input, output, args.type, args.null_str)


def run(input, output, type_strs, null_str):
    # Read headers
    headers = [util.unescape(val)
               for val in input.readline().strip().split('\t')]

    # Generate type processors
    if len(type_strs) == 0:
        types = [TYPES['str']] * len(headers)
    else:
        types = [TYPES[type_str] for type_str in type_strs]

    # Read input one line at a time
    for i, line in enumerate(input):
        lineno = i + 2  # i starts at 0 and we read a header line, so add 2

        # Read and parse the line
        try:
            val_strs = line.strip().split('\t')
            if len(val_strs) != len(headers):
                sys.stderr.write(
                    'line %s has %s columns, expected %s: %s\n' %
                    (lineno, len(val_strs), len(headers), line.strip()))
            values = [decode_value(val, type, null_str)
                      for type, val in zip(types, val_strs)]
        except Exception:
            sys.stderr.write('can\'t parse line %s: %s\n' % (lineno, line))
            sys.stderr.write(traceback.format_exc())
            continue

        # Build the doc
        doc = {}
        for header, value in zip(headers, values):
            place_value_at_path(doc, header, value)

        # Write it to the output
        output.write(json.dumps(doc, ensure_ascii=False))
        output.write('\n')


def decode_value(val, type, null_str):
    if val == null_str:
        return None
    else:
        return type(val)


def place_value_at_path(doc, path, value):
    parts = path.split('.')
    sub_doc = doc
    for p in parts[:-1]:
        if p not in sub_doc:
            sub_doc[p] = {}
        sub_doc = sub_doc[p]
    sub_doc[parts[-1]] = value
