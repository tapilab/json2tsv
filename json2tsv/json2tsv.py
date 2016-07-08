#!/usr/bin/env python
"""
Convert json to tsv from stdin by extracting the specified objects.

e.g., cat my.json | json2tsv id user.name
"""
import argparse
import json
import re
import sys

from . import open_read_utf8, open_write_utf8, my_unicode


def main():
    input = open_read_utf8(sys.stdin)
    output = open_write_utf8(sys.stdout)

    ap = argparse.ArgumentParser()
    ap.add_argument('fields', nargs='+', help='fields to print')
    ap.add_argument('--headers', action="store_true", help='fields to print')
    args = ap.parse_args()

    run(input, output, args.fields, args.headers)


def run(input, output, fields, headers):
    if headers:
        output.write('\t'.join(encode(f) for f in fields))
        output.write('\n')

    for i, line in enumerate(input):
        try:
            obj_or_list = json.loads(line)
        except Exception as e:
            sys.stderr.write('line %s is not valid JSON: %s\n' % (i + 1, e))
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
                             (i + 1, line))


def extract_row(fields, obj):
    return (encode(extract_value(field, obj)) for field in fields)


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


def rm_ws(s):
    """ Replace internal tabs/newlines with 5 spaces. """
    # return re.sub('[\n\t]', '    ', s)
    return re.sub('[\n\t]', '    ', my_unicode(s))


def encode(val):
    if isinstance(val, list) or isinstance(val, dict) or val is None:
        return json.dumps(val)
    else:
        return rm_ws(val)
