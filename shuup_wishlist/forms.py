# -*- coding: utf-8 -*-
# This file is part of Shuup Wishlist.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from shuup.core.models import ShopProduct
from shuup.utils.djangoenv import has_installed
from shuup_wishlist.models import Wishlist


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['name', 'privacy']

    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop', None)
        self.customer = kwargs.pop('customer', None)
        self.product_id = kwargs.pop('product_id', None)
        super(WishlistForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        if self.product_id:
            try:
                shop_product = ShopProduct.objects.get(pk=self.product_id, shop=self.shop)
            except ShopProduct.DoesNotExist as e:
                errors = [
                    ValidationError(_('Unknown error.'), code="unknown_error")
                ]
                if has_installed("raven.contrib.django.raven_compat"):
                    from raven.contrib.django.raven_compat.models import client
                    client.captureException()
            else:
                errors = shop_product.get_visibility_errors(self.customer)
            for error in errors:
                self.add_error(None, error)
        return super(WishlistForm, self).is_valid()
