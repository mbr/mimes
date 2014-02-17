from mimes import MIMEType

import pytest


fixtures = {
    # we do NOT support:
    # 1. comments -- e.g.: text/plain; charset=us-ascii (This is a comment)
    #
    # 2. value continuations
    # -- e.g.: Content-Type: message/external-body; access-type=URL;
    #           URL*0="ftp://";
    #           URL*1="cs.utk.edu/pub/moore/bulk-mailer/bulk-mailer.tar"
    #
    # 3. charset and language:
    # -- e.g. Content-Type: application/x-stuff;
    #          title*=us-ascii'en-us'This%20is%20%2A%2A%2Afun%2A%2A%2A
    #
    # because cgi.parse_headers does not support these either

    'application/json': {
        'type': 'application',
        'subtype': 'json',
        'private': False,
    },
    'text/plain': {
        'type': 'text',
        'subtype': 'plain',
        'private': False,
    },
    'application/xhtml+xml': {
        'type': 'application',
        'subtype': 'xhtml+xml',
        'private': False,
        'format': 'xml',
    },
    'text/plain; charset=us-ascii': {
        'type': 'text',
        'subtype': 'plain',
        'private': False,
        'parameters': {
            'charset': 'us-ascii',
        },
    },
    'text/plain; charset="us-ascii"': {
        'type': 'text',
        'subtype': 'plain',
        'private': False,
        'parameters': {
            'charset': 'us-ascii',
        },
    },
    ('message/external-body; access-type=URL; '
     'URL="ftp://cs.utk.edu/pub/moore/bulk-mailer/bulk-mailer.tar"'): {
         'type': 'message',
         'subtype': 'external-body',
         'private': False,
         'parameters': {
             'access-type': 'URL',
             'url': 'ftp://cs.utk.edu/pub/moore/bulk-mailer/bulk-mailer.tar',
         },
     },
    ('application/x-stuff; '
     "title*=This%20is%20%2A%2A%2Afun%2A%2A%2A"): {
         'type': 'application',
         'subtype': 'x-stuff',
         'private': True,
         'parameters': {
             'title': 'This is ***fun***',
         }
     },
    # FIXME: add vnd. types
}


@pytest.mark.parametrize('input,result', fixtures.items())
def test_parsing_fixtures(input, result):
    mt = MIMEType.from_string(input)

    assert mt.type == result['type']
    assert mt.subtype == result['subtype']
    assert mt.private == result['private']

    if mt.parameters:
        for k, v in result['parameters'].items():
            assert mt.parameters[k] == v
