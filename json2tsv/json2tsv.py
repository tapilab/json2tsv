#!/usr/bin/env python
"""
Convert json to tsv from stdin by extracting the specified objects.

e.g., cat my.json | json2tsv id user.name
"""
import argparse
import json
import re
import sys

if bytes == str:  # Python 2.7
    import codecs
    open_read_utf8 = lambda f: codecs.getreader('utf8')(f, 'replace')
    open_write_utf8 = lambda f: codecs.getwriter('utf8')(f, 'replace')
else:
    import io
    open_read_utf8 = lambda f: io.TextIOWrapper(f.buffer, 'utf8', 'replace')
    open_write_utf8 = lambda f: io.TextIOWrapper(f.buffer, 'utf8', 'replace')
    unicode = str


def rm_ws(s):
    """ Replace internal tabs/newlines with 5 spaces. """
    return re.sub('[\n\t]', '    ', unicode(s))


def main():
    output = open_write_utf8(sys.stdout)
    ap = argparse.ArgumentParser()
    ap.add_argument('fields', nargs='+', help='fields to print')
    ap.add_argument('--headers', action="store_true", help='fields to print')
    args = ap.parse_args()

    if args.headers:
        output.write('\t'.join(rm_ws(f) for f in args.fields))
        output.write('\n')

    for line in open_read_utf8(sys.stdin):
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
                        output.write('%s\t' % rm_ws(obj))
                    else:
                        output.write('%s\t' % rm_ws(jj[field]))
                output.write('\n')
        except Exception as e:
            sys.stderr.write('bad line %s\n' % e)
