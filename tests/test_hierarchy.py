from mimes import MIMEType


def test_simple():
    json = MIMEType('application', 'json')

    coljson = MIMEType('application', 'collection+json')
    apijson = MIMEType('application', 'api+json')

    assert json > coljson
    assert coljson < json
    assert json > apijson
    assert apijson < json

    assert not apijson > coljson
    assert not apijson < coljson
    assert not coljson > apijson
    assert not coljson < apijson


def test_equality_honors_parameters():
    json = MIMEType('application', 'json', parameters={'a': 1})
    json2 = MIMEType('application', 'json', parameters={'b': 2})
    json_ = MIMEType('application', 'json', parameters={'A': 1})

    assert json == json
    assert not json < json
    assert not json < json2
    assert json2 == json2
    assert json_ == json_

    assert json_ == json
    assert json == json_

    assert json != json2
    assert json2 != json
    assert json_ != json2
    assert json2 != json


def test_le():
    json = MIMEType('application', 'json', parameters={'a': 1})
    json2 = MIMEType('application', 'json', parameters={'b': 2})
    coljson = MIMEType('application', 'collection+json')

    assert json != coljson
    assert json2 != coljson

    assert json >= coljson
    assert json2 >= coljson
    assert coljson <= json

    assert json >= json2
