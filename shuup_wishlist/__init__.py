# -*- coding: utf-8 -*-
# This file is part of Shuup Wishlist.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import shuup.apps


class AppConfig(shuup.apps.AppConfig):
    name = __name__
    provides = {
        "xtheme_plugin": [__name__ + ".plugins:WishlistPlugin"],
        "xtheme_resource_injection": [__name__ + ".plugins:add_resources"],
        "front_urls": [
            "shuup_wishlist.urls:urlpatterns"
        ]
    }

default_app_config = __name__ + ".AppConfig"
