Shoop Wishlist
==============

This package implements wishlists
for the `Shoop <https://shoop.io/>`_ platform.

Copyright
---------

Copyright (C) 2012-2015 by Shoop Ltd. <contact@shoop.io>

Shoop is International Registered Trademark & Property of Shoop Ltd.,
Business ID: FI24815722, Business Address: Aurakatu 12 B, 20100 Turku,
Finland.

License
-------

Shoop Wishlist is published under the GNU Affero General Public License,
version 3 (AGPLv3). See the LICENSE file.

Running tests
-------------

You can run tests with `py.test <http://pytest.org/>`_.

Requirements for running tests:

* Your virtualenv needs to have Shoop installed.

* Project root must be in the Python path.  This can be done with:

  .. code:: sh

     pip install -e .

* The packages from ``testing_requirements.txt`` must be installed.

  .. code:: sh

     pip install -r testing_requirements.txt

To run tests, use command:

.. code:: sh

   py.test -v shoop_wishlist_tests
