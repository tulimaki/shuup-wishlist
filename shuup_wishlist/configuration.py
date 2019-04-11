# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from shuup import configuration
from shuup.front.admin_module.forms import (
    BaseSettingsForm, BaseSettingsFormPart
)


def is_dasbhoard_enabled(shop):
    return configuration.get(shop, "show_wishlist_on_dashboard", True)


def is_favorites_enabled(shop):
    return configuration.get(shop, "show_favorites_wishlist_on_dashboard", False)


class WishlistSettingsForm(BaseSettingsForm):
    title = _("Wishlist Settings")
    show_wishlist_on_dashboard = forms.BooleanField(
        label=_("Show wishlists on dashboard"),
        help_text=_("Setting this to false will hide wishlists from customer dashboard."),
        required=False,
        initial=True
    )
    show_favorites_wishlist_on_dashboard = forms.BooleanField(
        label=_("Show favorites wishlist on dashboard"),
        help_text=_("Combined with Wishlist Favorites Button plugin show favorites wishlist at dashboard."),
        required=False,
        initial=False
    )


class WishlistSettingsFormPart(BaseSettingsFormPart):
    form = WishlistSettingsForm
    name = "wishlist_settings"
    priority = 10
