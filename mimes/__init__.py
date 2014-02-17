from collections import OrderedDict
import cgi
import re
import urllib


class MIMEType(object):
    _TYPE_RE = re.compile(
        r'\s*(?P<type>[^\s]+)/(?P<subtype>[^\s;]+)\s*'  # application/foo
    )

    _TSPECIALS = {'(', ')', '<', '>', '@', ',', ';', ':', '\\', '"', '/', '[',
                  ']', '?', '='}

    def __init__(self, type, subtype, parameters=None):
        self.type = type
        self.subtype = subtype
        self.format = subtype[subtype.rfind('+')] if '+' in subtype else None
        self.parameters = parameters or OrderedDict()

    @property
    def private(self):
        return self.subtype.lower().startswith('x-')

    @classmethod
    def from_string(cls, s):
        value, params = cgi.parse_header(s)
        m = cls._TYPE_RE.match(value)

        if not m:
            raise ValueError('Not a valid MIME Content-Type string: '
                             '{!r}'.format(s))

        # RFC 2231, Section 4.
        parameters = {}
        for k, v in params.items():
            if k.endswith('*'):
                k = k[:-1]
                v = urllib.unquote(v)
            parameters[k] = v

        return cls(m.group('type'), m.group('subtype'), parameters)
