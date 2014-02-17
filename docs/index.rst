mimes
=====

The ``mimes`` library allows the parsing of *Content-Type* headers from various
MIME-enabled sources, such as HTTP or email headers. These headers contain an
`Internet media type <https://en.wikipedia.org/wiki/Internet_media_type>`_ and
are specified in RFCs `1049 <https://www.rfc-editor.org/rfc/rfc1049.txt>`_,
`2047 <https://www.rfc- editor.org/rfc/rfc2047.txt>`_ and `2231
<https://www.rfc- editor.org/rfc/rfc2231.txt>`_.


Parsing type strings
--------------------

Parsing a header string is rather simple, using the
:meth:`mimes.MIMEType.from_string` method::

  >>> from mimes import MIMEType
  >>> mt = MIMEType.from_string('application/collection+json')
  >>> mt.type
  'application'
  >>> mt.subtype
  'collection+json'
  >>> mt.format
  'json'

Extra parameters on types are also supported::

  >>> mt = MIMEType.from_string('application/vnd.custom_api; param1=foo; PARAM2="bar"')
  >>> mt.parameters
  {'param2': 'bar', 'param1': 'foo'}


Constructing type strings
-------------------------

Occasionally, it can be useful to construct header strings as well::

  >>> mt = MIMEType('application', 'xhtml+xml')
  >>> str(mt)
  'application/xhtml+xml'


Comparing compatible types
--------------------------

With the ``+format``-syntax, some media types can be considered a superset of
others. An application that can parse generic ``application/json``-data for
example will have no problems parsing anything that uses the JSON-format
as well. This is expressed using the inequality operators::

  >>> json = MIMEType('application', 'json')
  >>> coljson = MIMEType.from_string('application/collection+json')
  >>> json > coljson
  True
  >>> json == coljson
  False

A media type is strictly smaller than another media type if and only if both
types are of the same type (``application``), their subtypes are not equal
(``json`` vs ``collection+json``) and if the first type's format is exactly the
subtype of the second type (``json``). Parameters on both types are ignored.

Equality is checked by checking if the types are equal, including parameters.
Note that parameters are compared case-insensitive on keys, but
case-sensivitive on values::

  >>> mta = MIMEType.from_string('application/foo; param1=foo; param2=bar')
  >>> mtb = MIMEType.from_string('application/foo; PARAM2=bar; PARAM1=foo')
  >>> mta == mtb
  True
  >>> mtc = MIMEType.from_string('application/foo; param1=FOO; param2=bar')
  >>> mta == mtc
  False

