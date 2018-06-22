# -*- coding: utf-8 -*-
# This file is part of Shuup Wishlist.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import (
    add_product_to_wishlist, WishlistCreateView, WishlistCustomerDetailView,
    WishlistCustomerView, WishlistDeleteView, WishlistProductDeleteView,
    WishlistSearchView
)

urlpatterns = [
    url(r"wishlists/$", login_required(WishlistCustomerView.as_view()), name="personal_wishlists"),
    url(r"wishlists/search/$", login_required(WishlistSearchView.as_view()), name="search_wishlists"),
    url(r"^wishlist/(?P<pk>\d+)/$", login_required(WishlistCustomerDetailView.as_view()), name="wishlist_detail"),
    url(r"^wishlist/create/$", login_required(WishlistCreateView.as_view()), name="create_wishlist"),
    url(r"^wishlist/(?P<pk>\d+)/delete/$", login_required(WishlistDeleteView.as_view()), name="delete_wishlist"),
    url(r"^wishlist/(?P<wishlist_id>\w+)/product/(?P<shop_product_id>\d+)/$",
        login_required(add_product_to_wishlist), name="add_product_to_wishlist"),
    url(r"^wishlist/(?P<pk>\d+)/product/(?P<shop_product_pk>\d+)/remove/$",
        login_required(WishlistProductDeleteView.as_view()), name="remove_product_from_wishlist"),
]
