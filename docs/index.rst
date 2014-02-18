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
types are of the same type (``application``), are not equal and either the
first type's format is exactly the subtype of the second type
(``collection+json`` vs ``json``) or the first time has the same type and
subtype as the second without any parameters.

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


Finding suitable types through a MIMEGraph
------------------------------------------

mimes supports more complex searches for compatible internet media types. The
:class:`mimes.MIMEGraph` allows storing a list of types in a collection and
finding compatible types common. Two scenarios are common: Finding a supertype
or finding a subtype, both as specific as possible.

An example for the first scenario is a client sending an HTTP-request with a
body; the server accepts various media types, but not the one the client sent.
It is likely though that one of the types the server can handle is a supertype
of the type sent by the client. Example::

  >>> from mimes import MIMEGraph, MIMEType
  >>> g = MIMEGraph([MIMEType('application', 'json'), MIMEType('application', 'xml'), MIMEType('text', 'plain')])
  >>> g.find_super(MIMEType.from_string('application/collection+json'))
  MIMEType('application', 'json', OrderedDict())
  >>> g.find_super(MIMEType.from_string('application/xml'))
  MIMEType('application', 'xml', OrderedDict())

When sending a reply, the server could inspect the clients accept type headers
and determine to send it the most specific type the client can understand:

  >>> from mimes import MIMEGraph, MIMEType
  >>> a = MIMEGraph([MIMEType.from_string('application/json'), MIMEType.from_string('application/problem+json')])
  >>> a.find_sub(MIMEType.from_string('application/json'))
  MIMEType('application', 'problem+json', OrderedDict())
