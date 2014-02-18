from mimes import MIMEType, MIMEGraph


import pytest


@pytest.fixture
def ms():
    return MIMEGraph.from_strings('application/json',
                                  'application/collection+json',
                                  'text/plain',
                                  'application/collection+json; version=1',
                                  'application/collection+json; version=2'
                                  )


def test_parse_incoming(ms):
    # use case: given a list of parsers, find one for the client input
    assert ms.get_closest_fit(
        MIMEType.from_string('application/collection+json; version=3')
    ) == MIMEType.from_string('application/collection+json')

    assert ms.get_closest_fit(
        MIMEType.from_string('application/collection+json; version=1')
    ) == MIMEType.from_string('application/collection+json; version=1')

    assert ms.get_closest_fit(
        MIMEType.from_string('application/json')
    ) == MIMEType.from_string('application/json')

    assert ms.get_closest_fit(
        MIMEType.from_string('application/api+json')
    ) == MIMEType.from_string('application/json')

    assert ms.get_closest_fit(
        MIMEType.from_string('image/jpeg')
    ) is None
