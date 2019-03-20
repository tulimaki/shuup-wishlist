# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
import shuup.apps


class AppConfig(shuup.apps.AppConfig):
    name = __name__
    provides = {
        "xtheme_plugin": [
            __name__ + ".plugins:WishlistPlugin",
            __name__ + ".plugins:WishlistSmallButtonPlugin",
        ],
        "customer_dashboard_items": [
            __name__ + '.dashboard_items:WishlistItem',
        ],
        "xtheme_resource_injection": [__name__ + ".plugins:add_resources"],
        "front_urls": [
            "shuup_wishlist.urls:urlpatterns"
        ]
    }


default_app_config = __name__ + ".AppConfig"
