from collections import OrderedDict
import cgi
import re

try:
    from urllib import unquote, quote
except ImportError:
    from urllib.parse import unquote, quote


class MIMEType(object):
    _TYPE_RE = re.compile(
        r'\s*(?P<type>[^\s]+)/(?P<subtype>[^\s;]+)\s*'  # application/foo
    )

    def __init__(self, type, subtype, parameters=None):
        self.type = type
        self.subtype = subtype
        self.parameters = parameters or OrderedDict()

    @property
    def _param_string(self):
        if not self.parameters:
            return ''

        buf = []
        for k, v in self.parameters.items():
            v = str(v)
            k = str(k).lower()
            vs = quote(v)

            if vs != v:
                k += '*'

            buf.append('; {}={}'.format(k, vs))
        return ''.join(buf)

    def _get_lower_params(self):
        return {
            k.lower(): v for k, v in self.parameters.items()
        }

    @property
    def format(self):
        return self.subtype[self.subtype.rfind('+')+1:] if '+' in self.subtype\
            else None

    @property
    def vendor(self):
        return self.subtype.lower().startswith('vnd.')

    @property
    def personal(self):
        return self.subtype.lower().startswith('prs.')

    @property
    def private(self):
        return (self.subtype.lower().startswith('x-') or
                self.subtype.lower().startswith('x.'))

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
                v = unquote(v)
            parameters[k] = v

        return cls(m.group('type'), m.group('subtype'), parameters)

    def __str__(self):
        return '{self.type}/{self.subtype}{self._param_string}'.format(
            self=self
        )

    def __repr__(self):
        return ('{self.__class__.__name__}({self.type!r}, {self.subtype!r},'
                ' {self.parameters!r}'.format(self=self))

    # ordering
    def __eq__(self, other):
        return (self.type == other.type and
                self.subtype == other.subtype and
                self._get_lower_params() == other._get_lower_params()
                )

    def __gt__(self, other):
        if self == other:
            return False

        if self.type == other.type:
            if self.subtype == other.subtype and not self.parameters:
                return True
            if self.subtype == other.format:
                return True

        return False

    def __ge__(self, other):
        return self == other or self > other


class MIMESet(set):
    def get_most_specific(self, t):
        candidates = set()

        for c in self:
            if c == t:
                return c
            if t < c:
                candidates.add(c)

        if not candidates:
            return None

        # no exact match found, remove all elements that have more specific
        # children in the candidate set
        valid = candidates.copy()
        for cand in candidates:
            for other in candidates:
                if cand > other:
                    # discard candidate
                    valid.remove(cand)
                    continue

        # rank candidates according to mimestring
        return sorted(valid, key=str, reverse=True)[0]

    @classmethod
    def from_strings(cls, *ss):
        return cls([MIMEType.from_string(s) for s in ss])
