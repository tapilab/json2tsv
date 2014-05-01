json2tsv
========

|image|

|image|

|image|

Convert json to tab-separated format. Read from STDOUT and write to
STDOUT. E.g.

::

    $ echo '[{"id":"123", "user":{"name":"mary", "gender":"female"}}, {"id":"124", "user":{"name":"mark", "gender":"male"}}]' | json2tsv id user.name user.gender
    123     mary    female
    124     mark    male

-  Free software: BSD license
-  Documentation: http://json2tsv.rtfd.org.

.. |image| image:: https://badge.fury.io/py/json2tsv.png%0A%20:target:%20http://badge.fury.io/py/json2tsv
.. |image| image:: https://travis-ci.org/aronwc/json2tsv.png?branch=master%0A%20%20%20%20%20:target:%20https://travis-ci.org/aronwc/json2tsv
.. |image| image:: https://pypip.in/d/json2tsv/badge.png%0A%20%20%20%20%20:target:%20https://pypi.python.org/pypi/json2tsv
