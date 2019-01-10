.. image:: https://travis-ci.org/shuup/shuup-wishlist.svg?branch=master
    :target: https://travis-ci.org/shuup/shuup-wishlist
.. image:: https://coveralls.io/repos/github/shuup/shuup-wishlist/badge.svg?branch=master
    :target: https://coveralls.io/github/shuup/shuup-wishlist?branch=master

Shuup Wishlist
==============

This package implements wishlists
for the `Shuup <https://www.shuup.com/>`_ platform.

Copyright
---------

Copyright (C) 2012-2019 by Shoop Commerce Ltd. <support@shuup.com>

Shuup is International Registered Trademark & Property of Shoop Commerce Ltd.,
Business ID: FI27184225,
Business Address: Iso-Roobertinkatu 20-22, 00120 HELSINKI, Finland.

License
-------

Shuup Wishlist is published under Open Software License version 3.0 (OSL-3.0).
See the LICENSE file distributed with Shuup.

Some external libraries and contributions bundled with Shuup may be
published under other compatible licenses. For these, please
refer to the licenses included within each package.

Chat
----

We have a Gitter chat room for Shuup.  Come chat with us!  |Join chat|

.. |Join chat| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/shuup/shuup

Getting Started with Shuup development
--------------------------------------

See `Getting Started with Shuup Development
<http://shuup.readthedocs.io/en/latest/howto/getting_started_dev.html>`__.

Contributing to Shuup
---------------------

Interested in contributing to Shuup? Please see our `Contribution Guide
<https://www.shuup.com/contributions/>`__.

Documentation
-------------

Shuup documentation is available online at `Read the Docs
<http://shuup.readthedocs.org/>`__.

Running tests
-------------

You can run tests with `py.test <http://pytest.org/>`_.

Requirements for running tests:

* Your virtualenv needs to have Shuup installed.

* Project root must be in the Python path.  This can be done with:

  .. code:: sh

     pip install -e .

* The packages from ``testing_requirements.txt`` must be installed.

  .. code:: sh

     pip install -r testing_requirements.txt

To run tests, use command:

.. code:: sh

   py.test -v shuup_wishlist_tests

Building a release
------------------

* `python setup.py bdist_wheel`
