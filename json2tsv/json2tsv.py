#!/usr/bin/env python
"""
Convert json to tsv from stdin by extracting the specified objects.

e.g., cat my.json | json2tsv id user.name
"""
import argparse
import json
import sys

from . import util


def main():
    parser = argparse.ArgumentParser(
        description='Convert json to tsv from stdin by extracting the ' +
                    'specified objects.')
    parser.add_argument('fields', nargs='+', help='fields to print')
    parser.add_argument(
        '--headers', action="store_true", help='print headers as first row')
    args = parser.parse_args()

    input = util.read(sys.stdin)
    output = util.write(sys.stdout)

    run(input, output, args.fields, args.headers)


def run(input, output, fields, headers):
    # Write headers
    if headers:
        output.write('\t'.join(util.encode(f) for f in fields))
        output.write('\n')

    # Write lines from input
    for i, line in enumerate(input):
        lineno = i + 1  # i starts at 0, so add 1

        # Try to read some JSON
        try:
            obj_or_list = json.loads(line)
        except Exception as e:
            sys.stderr.write('line %s is not valid JSON: %s\n' % (lineno, e))
            continue

        if isinstance(obj_or_list, list):
            json_list = obj_or_list
            for obj in json_list:
                output.write('\t'.join(extract_row(fields, obj)))
                output.write('\n')
        elif isinstance(obj_or_list, dict):
            obj = obj_or_list
            output.write('\t'.join(extract_row(fields, obj)))
            output.write('\n')
        else:
            sys.stderr.write('line %s is not a JSON list or object: %r\n' %
                             (lineno, line))


def extract_row(fields, obj):
    return (util.encode(extract_value(field, obj)) for field in fields)


def extract_value(field, obj):
    """
    >>> js = {'id': 123, 'user': {'name': 'mary'}}
    >>> extract_value('id', js)
    123
    >>> extract_value('user', js)
    {'name': 'mary'}
    >>> extract_value('user.name', js)
    'mary'
    >>> extract_value('-', js)
    {'id': 123, 'user': {'name': 'mary'}}
    >>> extract_value('not_valid', js)
    """
    if field == "-":  # Special case -- return whole json object
        return obj
    parts = field.split('.')
    for p in parts:
        obj = obj.get(p)
        if obj is None:
            break
    return obj
