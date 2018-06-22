# -*- coding: utf-8 -*-
# This file is part of Shuup Wishlist.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from shuup.core.models import get_person_contact, Shop
from shuup.testing.factories import create_product, get_default_shop
from shuup_wishlist.forms import WishlistForm

from .fixtures import regular_user

regular_user = regular_user  # noqa


@pytest.mark.django_db
def test_form(admin_user, rf):
    shop = get_default_shop()
    customer = get_person_contact(admin_user)
    customer.save()
    product = create_product("test", shop=shop)
    shop_product = product.get_shop_instance(shop)
    form = WishlistForm(
        data={
            "name": "foo",
            "privacy": 0,
            "shop_product_id": product.id
        }, shop=shop, customer=customer, shop_product_id=shop_product.id)
    form.full_clean()
    assert form.is_valid()
    assert not form.errors
    assert form.is_bound
    form.is_valid()  # shouldn't raise


@pytest.mark.django_db
def test_invalid_form(admin_user, rf):
    shop = get_default_shop()
    customer = get_person_contact(admin_user)
    customer.save()
    shop2 = Shop.objects.create(identifier="test2")
    product = create_product("test", shop=shop)
    shop_product = product.get_shop_instance(shop)
    form = WishlistForm(
        data={
            "name": "foo",
            "privacy": 0,
            "shop_product_id": product.id
        }, shop=shop2, customer=customer, shop_product_id=shop_product.id)
    form.full_clean()
    assert not form.is_valid()
    assert form.errors
    assert form.is_bound
    form.is_valid()  # shouldn't raise
