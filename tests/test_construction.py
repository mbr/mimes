from collections import OrderedDict

from mimes import MIMEType

import pytest

mts = {
    'application/json': MIMEType('application', 'json'),
    'application/xhtml+xml': MIMEType('application', 'xhtml+xml'),
    'application/foo; bar=1; baz=2': MIMEType(
        'application', 'foo', parameters=OrderedDict([('bar', 1), ('baz', 2)])
    ),
    'application/foo; bar*=strange%20stuff': MIMEType(
        'application', 'foo', parameters={'BAR': 'strange stuff'},
    )
}


@pytest.mark.parametrize('output,mt', mts.items())
def test_parsing_fixtures(output, mt):
    assert output == str(mt)
