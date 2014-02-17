mimes
=====

An internet MIME-message is usually accompanied by a content-type string like
``application/json``, ``text/plain`` or more complex types like
``application/xhtml+xml``. The mimetype declaration spec has been extended in
recent years, for example by adding vendor-specific types (like
``application/vnd.mycompany.myapp+json``). As a result, some mimetypes can be
considered a supertype - the example could easily also be at least partially
understood by a program that parses plain ``application/json``.

The mimetypes library allows parsing a mimetype to discern its type and
subtype and other attributes. It also allows comparing these types to find out
if one is a supertype of another.
