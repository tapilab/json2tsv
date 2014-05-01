#!/usr/bin/env python
"""
Convert json to tsv from stdin by extracting the specified objects.

e.g., cat my.json | json2tsv id user.name
"""
import argparse
import codecs
import json
import re
import sys


def rm_ws(s):
    """ Replace internal tabs/newlines with 5 spaces. """
    return re.sub('[\n\t]', '    ', unicode(s))


def main():
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    ap = argparse.ArgumentParser()
    ap.add_argument('fields', nargs='+', help='fields to print')
    args = ap.parse_args()

    for line in sys.stdin:
        try:
            j = json.loads(line)
            if type(j) is dict:  # as opposed to a list of dicts.
                j = [j]
            for jj in j:
                for field in args.fields:
                    if '.' in field:
                        parts = field.split('.')
                        obj = jj
                        for p in parts:
                            obj = obj[p]
                        sys.stdout.write('%s\t' % rm_ws(obj))
                    else:
                        sys.stdout.write('%s\t' % rm_ws(jj[field]))
                sys.stdout.write('\n')
        except Exception as e:
            sys.stderr.write('bad line %s\n' % e)
