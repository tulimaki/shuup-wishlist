# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
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
        self.shop_product_id = kwargs.pop('shop_product_id', None)
        super(WishlistForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        if self.shop_product_id:
            errors = []

            try:
                shop_product = ShopProduct.objects.get(pk=self.shop_product_id)
            except ShopProduct.DoesNotExist as e:
                errors.append(ValidationError(_('Invalid shop product.'), code="invalid-shop-product"))

                if has_installed("raven.contrib.django.raven_compat"):
                    from raven.contrib.django.raven_compat.models import client
                    client.captureException()

            if shop_product.shop != self.shop:
                errors.append(ValidationError(_('Invalid shop.'), code="invalid-shop"))

            errors.extend(list(shop_product.get_visibility_errors(self.customer)))
            for error in errors:
                self.add_error(None, error)

        return super(WishlistForm, self).is_valid()
