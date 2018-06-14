# -*- coding: utf-8 -*-
# This file is part of Shuup Wishlist.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from shuup.core.models import get_person_contact
from shuup.testing.factories import get_default_shop, get_default_shop_product
from shuup.testing.utils import apply_request_middleware
from shuup_wishlist.models import Wishlist, WishlistPrivacy
from shuup_wishlist.plugins import WishlistPlugin


@pytest.mark.django_db
def test_wishlist_plugin_get_context(rf, admin_user):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    product = get_default_shop_product()
    wishlist = Wishlist.objects.create(shop=shop, customer=person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    request = apply_request_middleware(rf.get("/"), shop=shop, user=person.user, shop_product=product)
    plugin = WishlistPlugin({})
    context = plugin.get_context_data({'request': request})

    assert 'wishlists' in context
    assert 'shop_product' in context
    assert context['wishlists'].count() == 1
    assert context['wishlists'][0].name == wishlist.name
