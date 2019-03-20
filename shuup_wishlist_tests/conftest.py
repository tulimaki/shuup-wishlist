# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
import pytest


# always make ShopProduct id different from Product id
@pytest.fixture(autouse=True)
def break_shop_product_id_sequence(db):
    from shuup.core.models import ShopProduct
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("INSERT INTO SQLITE_SEQUENCE (name, seq) values ('%s', 1500)" % ShopProduct._meta.db_table)
