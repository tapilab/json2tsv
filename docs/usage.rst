========
Usage
========

::

    $ echo '[{"id":"123", "user":{"name":"mary", "gender":"female"}}, {"id":"124", "user":{"name":"mark", "gender":"male"}}]' | json2tsv id user.name user.gender
    123     mary    female
    124     mark    male
