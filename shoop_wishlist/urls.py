# -*- coding: utf-8 -*-
# This file is part of Shoop Wishlist.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r"wishlists/$",
        views.CustomerWishlistsView.as_view(),
        name="personal_wishlists"),
    url(r"wishlist/(?P<pk>\d+)/$",
        views.CustomerWishlistDetailView.as_view(),
        name="wishlist_detail"),
    url(r"^wishlist/create/$",
        views.WishlistCreate.as_view(),
        name="create_wishlist"),
    url(r"^wishlist/(?P<pk>\d+)/delete/$",
        views.WishlistDelete.as_view(),
        name="delete_wishlist"),
    url(r"^wishlist/(?P<wishlist_id>\d+)/product/(?P<product_id>\d+)/$",
        views.add_product_to_wishlist,
        name="add_product_to_wishlist"),
    url(r"^wishlist/(?P<pk>\d+)/product/(?P<product_pk>\d+)/remove/$",
        views.WishlistProductDelete.as_view(),
        name="remove_product_from_wishlist"),
)
