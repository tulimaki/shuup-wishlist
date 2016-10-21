# -*- coding: utf-8 -*-
# This file is part of Shuup Wishlist.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.conf.urls import patterns, url

from .views import (
    add_product_to_wishlist, CustomerWishlistDetailView, CustomerWishlistsView,
    WishlistCreateView, WishlistDeleteView, WishlistProductDeleteView,
    WishlistSearchView
)

urlpatterns = patterns(
    '',
    url(r"wishlists/$", CustomerWishlistsView.as_view(), name="personal_wishlists"),
    url(r"wishlists/search/$", WishlistSearchView.as_view(), name="search_wishlists"),
    url(r"^wishlist/(?P<pk>\d+)/$", CustomerWishlistDetailView.as_view(), name="wishlist_detail"),
    url(r"^wishlist/create/$", WishlistCreateView.as_view(), name="create_wishlist"),
    url(r"^wishlist/(?P<pk>\d+)/delete/$", WishlistDeleteView.as_view(), name="delete_wishlist"),
    url(r"^wishlist/(?P<wishlist_id>\w+)/product/(?P<product_id>\d+)/$",
        add_product_to_wishlist, name="add_product_to_wishlist"),
    url(r"^wishlist/(?P<pk>\d+)/product/(?P<product_pk>\d+)/remove/$",
        WishlistProductDeleteView.as_view(), name="remove_product_from_wishlist"),
)
