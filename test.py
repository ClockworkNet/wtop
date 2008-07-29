import re


def compile_derivs(commands):
    cols = re.compile(r'(?:(qs)\(([a-z\*1]+|)\)|([a-z]+))')
    fields = cols.findall(commands)
    return fields


print compile_derivs('mx,qs(blink)')


def classify(url): return 'foo'


def mk_field_fn(field, dfn):
    def fn(record):
        if not record.has_key(field):
            record[field] = dfn(record)
        return record[field]
    return fn

all_fns = {
    'request':     (lambda r: r['request']),
    'url':         mk_field_fn('url',     (lambda r: all_fns['request'](record)[1])),
    'qs(bar)':     mk_field_fn('qs(bar)', (lambda r: re.compile(r'\bbar=([^&]+)').findall(all_fns['url'](record)))),
    'class':       mk_field_fn('class',   (lambda r: classify(all_fns['url'](record)))),
}

record = {'request': ('GET', '/foo.html?bar=f&bar=foo', 'HTTP')}

print all_fns['qs(bar)'](record)

print record


#jessie shell



# the ideal thing would be to have two simple languages: one for filtering and one for output.
# each would compile to a function that takes in an entire "raw" record and outputs a processed record.
# the simplest "function" would be something like 'ua', which simply copies the user-agent field.
# more complex would be 'url', which requires that the request field be based and extract the 2nd
# field. 'class' would call 'url', which calls 'request', etc. That part is fairly simple.
# opmtimization is difficult, for two reasons: we don't want to parse all of the raw fields defined
# in the log format if they are not called for, and we need to make sure that we're not parsing the
# same things again and again.
def compile_derivs(commands):
    cols = re.compile(r'(?:(qs)\(([a-z\*1]+|)\)|([a-z]+))')
    fields = cols.findall(commands)
    return fields


def url(record):
    if not record.has_key('url'):
        record['url'] = request(record)[1]
    return record['url']


def url(record):
    if not record.has_key('url'):
        record['url'] = all_fns['request'](record)[1]
    return record['url']

def mk_field_fn(field, fn):
    def fn(record):
        if not record.has_key(field):
            record[field] = fn(record)
        return record[field]

all_fns = {
    'request':     (lambda r: r['request']),
    'url':         mk_field_fn('url', (lambda r: all_fns['request'](record)[1]))
}
