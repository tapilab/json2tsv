#!/usr/bin/env python
"""
Convert tsv to json from stdin, assuming first line is header.

e.g., cat my.tsv | tsv2json
"""
import json
import sys

from . import open_read_utf8, open_write_utf8


def main():
    output = open_write_utf8(sys.stdout)
    header = None
    for line in open_read_utf8(sys.stdin):
        try:
            columns = line.strip().split('\t')
            if not header:
                header = columns
            else:
                d = {}
                for field, value in zip(header, columns):
                    if '.' in field:
                        parts = field.split('.')
                        r = d
                        for p in parts[:-1]:
                            if p not in r:
                                r[p] = {}
                            r = r[p]
                        r[parts[-1]] = value
                    else:
                        d[field] = value
                output.write('%s\n' % json.dumps(d, ensure_ascii=False))
        except Exception as e:
            sys.stderr.write('bad line %s\n' % e)
            print(sys.exc_info()[0])
