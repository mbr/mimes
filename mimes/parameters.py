import re

MIME_SPECIAL_CHARS = re.escape(r'()<>@,;:\"/[]?=]')
MIME_TOKEN_CHARS = 'A-Za-z0-9' + re.escape(r"""!#$%&'*+-._`{}|~""")

_QUOTED_STRING_INSIDE = r'(?:[{}\s]|\\[{}])'.format(MIME_TOKEN_CHARS,
                                                    MIME_SPECIAL_CHARS)

_LEXEMES = {
    'QUOTED_STRING': r'(?<!\\)"({}*)(?<!\\)"'.format(_QUOTED_STRING_INSIDE),
    'TSPECIAL': r'([{}])'.format(MIME_SPECIAL_CHARS),
    'TOKEN': r'([{}])+'.format(MIME_TOKEN_CHARS),
    'WHITESPACE': r'(\s+)',
}


def build_expr():
    regex = []
    for name, expr in _LEXEMES.items():
        regex.append(r'(?P<{}>{})'.format(name, expr))
    return '|'.join(regex)

LEX_REGEX = re.compile(build_expr())


def lex(s):
    for m in LEX_REGEX.finditer(s):
        yield (m.lastgroup, m.group(m.lastgroup))

    yield ('EOS',)


class Parser(object):
    def __init__(self, src):
        self._tokens = lex(src)
        self.next_token()

    def next_token(self):
        try:
            self._buf = self._tokens.next()
        except StopIteration:
            raise ValueError('Unexepected end of input')

    def accept(token_type, value=None):
        if self._buf[0] == token and (value is None or self._buf[1] == value):
            self.next_token()
            return self._buf[1]

        return None

    def expect(token_type, value=None):
        v = self.accept()

        raise ValueError('Expected {}<{!r}>'.format(token_type, value))
