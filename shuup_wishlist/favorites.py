# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.utils.translation import ugettext_lazy as _

from shuup_wishlist.models import Wishlist


def get_favorites_list(shop, customer):
    if not (customer and shop):
        return
    return Wishlist.objects.get_or_create(
        shop=shop, customer=customer, name=_("Favorites"))[0]
