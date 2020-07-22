# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.db.models import Count
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from shuup.front.utils.dashboard import DashboardItem
from shuup_wishlist.models import Wishlist

from .configuration import is_dasbhoard_enabled, is_favorites_enabled
from .favorites import get_favorites_list


class WishlistItem(DashboardItem):
    template_name = "shuup_wishlist/dashboard/dashboard_item.jinja"
    title = _("Wishlists")
    icon = "fa fa-heart"
    view_text = _("Show all")
    _url = "shuup:personal_wishlists"

    def show_on_menu(self):
        return is_dasbhoard_enabled(self.request.shop)

    def show_on_dashboard(self):
        return is_dasbhoard_enabled(self.request.shop)

    def get_context(self):
        context = super(WishlistItem, self).get_context()
        context["wishlists"] = Wishlist.objects.filter(
            customer=self.request.customer,
            shop=self.request.shop
        ).annotate(product_count=Count('products'))[:5]
        return context


class FavoritesItem(DashboardItem):
    title = _("Favorites")
    icon = "fa fa-heart"

    def show_on_menu(self):
        return is_favorites_enabled(self.request.shop)

    def show_on_dashboard(self):
        return False

    @property
    def url(self):
        shop = self.request.shop
        customer = self.request.customer
        favorites_list = get_favorites_list(shop, customer)
        if favorites_list:
            return reverse("shuup:wishlist_detail", kwargs={"pk": favorites_list.pk})
