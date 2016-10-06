# -*- coding: utf-8 -*-
# This file is part of Shuup Wishlist.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from shuup.xtheme.resources import add_resource
from shuup_wishlist.models import Wishlist

try:
    from shuup.xtheme import TemplatedPlugin
except:
    from shuup.xtheme.plugins import TemplatedPlugin


def add_resources(context, content):
    add_resource(context, "head_end", "%sshuup_wishlist/css/style.css" % settings.STATIC_URL)
    add_resource(context, "body_end", "%sshuup_wishlist/js/lib.js" % settings.STATIC_URL)
    add_resource(context, "body_end", "%sshuup_wishlist/js/flash_message.js" % settings.STATIC_URL)


class WishlistPlugin(TemplatedPlugin):
    identifier = "shuup_wishlist.wishlist_button"
    name = _("Wishlist Plugin")
    template_name = "shuup_wishlist/wishlist_action_button.jinja"
    required_context_variables = ['shop_product']

    def __init__(self, config):
        super(WishlistPlugin, self).__init__(config)

    def render(self, context):
        add_resource(context, "body_end", "%sshuup_wishlist/js/script.js" % settings.STATIC_URL)
        return super(WishlistPlugin, self).render(context)

    def get_context_data(self, context):
        context = super(WishlistPlugin, self).get_context_data(context)
        context["wishlists"] = Wishlist.objects.filter(
            shop=context['request'].shop,
            customer=context['request'].customer
        )
        return context
