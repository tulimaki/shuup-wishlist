# -*- coding: utf-8 -*-
# This file is part of Shoop Wishlist.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import shoop.apps


class AppConfig(shoop.apps.AppConfig):
    name = __name__
    provides = {
        "xtheme_plugin": [__name__ + ".plugins:WishlistPlugin"],
        "xtheme_resource_injection": [__name__ + ".plugins:add_resources"],
        "front_urls": [
            "shoop_wishlist.urls:urlpatterns"
        ]
    }

default_app_config = __name__ + ".AppConfig"
