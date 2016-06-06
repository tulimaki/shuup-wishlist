# -*- coding: utf-8 -*-
# This file is part of Shoop Wishlist.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
from enumfields import Enum, EnumIntegerField

from shoop.core.models import Contact, Product, Shop
from shoop.core.models._base import ShoopModel


class WishlistPrivacy(Enum):
    PUBLIC = 0
    SHARED = 1
    PRIVATE = 2

    class Labels:
        PUBLIC = _('public')
        SHARED = _('shared')
        PRIVATE = _('private')


class Wishlist(ShoopModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name=_('shop'))
    customer = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name=_('customer'))
    name = models.CharField(verbose_name=_('name'), max_length=50)
    privacy = EnumIntegerField(WishlistPrivacy, default=WishlistPrivacy.PRIVATE, verbose_name=_('privacy'))
    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('created on'))
    products = models.ManyToManyField(Product, related_name='wishlists', verbose_name=_('products'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Wishlist')
        verbose_name_plural = _('Wishlists')
