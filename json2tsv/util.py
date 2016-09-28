import json

if bytes == str:  # Python 2.7
    import codecs
    read = lambda f: codecs.getreader('utf8')(f, 'replace')
    write = lambda f: codecs.getwriter('utf8')(f, 'replace')
    unicode = unicode  # flake8: noqa
else: # Python 3.x
    import io
    read = lambda f: io.TextIOWrapper(f.buffer, 'utf8', 'replace')
    write = lambda f: io.TextIOWrapper(f.buffer, 'utf8', 'replace')
    unicode = str


def escape(val):
    """Escape tabs and newlines"""
    # return re.sub('[\n\t]', '    ', s)
    u = unicode(val)
    return u.replace('\t', '\\t').replace('\n', "\\n")

def encode(val):
    if isinstance(val, list) or isinstance(val, dict) or val is None:
        return json.dumps(val)
    else:
        return escape(val)

def unescape(val):
    u = unicode(val)
    return u.replace('\\t', '\t').replace('\\n', "\n")
