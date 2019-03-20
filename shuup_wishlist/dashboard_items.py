# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from shuup.front.utils.dashboard import DashboardItem
from shuup_wishlist.models import Wishlist


class WishlistItem(DashboardItem):
    template_name = "shuup_wishlist/dashboard/dashboard_item.jinja"
    title = _("Wishlists")
    icon = "fa fa-heart"
    view_text = _("Show all")
    _url = "shuup:personal_wishlists"

    def get_context(self):
        context = super(WishlistItem, self).get_context()
        context["wishlists"] = Wishlist.objects.filter(
            customer=self.request.customer,
            shop=self.request.shop
        ).annotate(product_count=Count('products'))[:5]
        return context
