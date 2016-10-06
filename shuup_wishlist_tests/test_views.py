# -*- coding: utf-8 -*-
# This file is part of Shuup Wishlist.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import json

import pytest
from django.db.models import ObjectDoesNotExist
from django.http import Http404

from shuup.core.models import get_person_contact
from shuup.testing.factories import get_default_product, get_default_shop
from shuup.testing.utils import apply_request_middleware
from shuup_tests.utils.fixtures import regular_user
from shuup_wishlist.models import Wishlist, WishlistPrivacy
from shuup_wishlist.views import (
    add_product_to_wishlist, CustomerWishlistDetailView, CustomerWishlistsView,
    WishlistCreate, WishlistDelete, WishlistProductDelete
)

regular_user = regular_user  # noqa


@pytest.mark.django_db
def test_wishlist_create_invalid(admin_user, rf):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    view_func = WishlistCreate.as_view()
    request = apply_request_middleware(rf.post("/"), shop=shop, customer=person)
    response = view_func(request)

    assert response.status_code == 400


@pytest.mark.django_db
def test_wishlist_create(admin_user, rf):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    view_func = WishlistCreate.as_view()
    request = rf.post("/", {"name": "foo", "privacy": 0})
    request = apply_request_middleware(request, shop=shop, customer=person)
    response = view_func(request)
    data = json.loads(response.content)
    wishlists = Wishlist.objects.filter(shop=shop, customer=person).all()
    wishlist = wishlists.first()

    assert response.status_code == 200
    assert data.get('name', '') == 'foo'
    assert data.get('created', False)
    assert str(wishlist) == wishlist.name
    assert wishlists.count() == 1
    assert wishlist.name == 'foo'
    assert wishlist.privacy == WishlistPrivacy.PUBLIC
    assert wishlist.products.count() == 0


@pytest.mark.django_db
def test_wishlist_create_with_product(admin_user, rf):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    product = get_default_product()
    view_func = WishlistCreate.as_view()
    request = rf.post("/", {"name": "foo", "privacy": 0, "product_id": product.id})
    request = apply_request_middleware(request, shop=shop, customer=person)
    response = view_func(request)
    data = json.loads(response.content)
    wishlists = Wishlist.objects.filter(shop=shop, customer=person).all()
    wishlist = wishlists.first()

    assert response.status_code == 200
    assert data.get('name', '') == 'foo'
    assert data.get('created', False)
    assert data.get('product_name', '') == product.name
    assert wishlists.count() == 1
    assert wishlist.name == 'foo'
    assert wishlist.privacy == WishlistPrivacy.PUBLIC
    assert wishlist.products.count() == 1


@pytest.mark.django_db
def test_wishlist_create_with_deleted_product(admin_user, rf):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    product = get_default_product()
    product.soft_delete(admin_user)
    view_func = WishlistCreate.as_view()
    request = rf.post("/", {"name": "foo", "privacy": 0, "product_id": product.id})
    request = apply_request_middleware(request, shop=shop, customer=person)
    response = view_func(request)

    assert response.status_code == 400


@pytest.mark.django_db
def test_wishlist_create_get_context_data(admin_user, rf):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    view_func = WishlistCreate.as_view()
    request = apply_request_middleware(rf.get("/?product_id=1"), shop=shop, customer=person)
    response = view_func(request)

    assert response.status_code == 200
    assert 'product_id' in response.context_data.keys()
    assert response.context_data.get('product_id') == '1'


@pytest.mark.django_db
def test_add_product_to_wishlist_invalid_method(rf):
    request = apply_request_middleware(rf.get("/"))
    response = add_product_to_wishlist(request, 0, 0)

    assert response.status_code == 405


@pytest.mark.django_db
def test_add_product_to_wishlist_unauthorized(rf, admin_user, regular_user):
    request = apply_request_middleware(rf.post("/"))
    response = add_product_to_wishlist(request, 0, 0)

    assert response.status_code == 403

    shop = get_default_shop()
    person = get_person_contact(regular_user)
    product = get_default_product()
    other_person = get_person_contact(admin_user)
    wishlist = Wishlist.objects.create(shop=shop, customer=other_person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    request = apply_request_middleware(rf.post("/"), customer=person)
    response = add_product_to_wishlist(request, wishlist.id, product.id)

    assert response.status_code == 400


@pytest.mark.django_db
def test_add_product_to_wishlist(rf, admin_user):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    product = get_default_product()
    wishlist = Wishlist.objects.create(shop=shop, customer=person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    request = apply_request_middleware(rf.post("/"), customer=person)
    response = add_product_to_wishlist(request, wishlist.id, product.id)
    data = json.loads(response.content)

    assert response.status_code == 200
    assert data.get('product_name', '') == product.name
    assert data.get('created', False)
    assert wishlist.products.count() == 1


@pytest.mark.django_db
def test_personal_wishlists(rf, admin_user, regular_user):
    shop = get_default_shop()
    admin_person = get_person_contact(admin_user)
    person = get_person_contact(regular_user)
    product = get_default_product()

    wishlist = Wishlist.objects.create(shop=shop, customer=person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(product)
    Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PUBLIC)

    view_func = CustomerWishlistsView.as_view()
    request = apply_request_middleware(rf.get("/"), customer=person)
    response = view_func(request)

    assert response.status_code == 200
    assert 'customer_wishlists' in response.context_data
    assert response.context_data['customer_wishlists'].count() == 1


@pytest.mark.django_db
def test_view_own_wishlist_detail(rf, regular_user):
    shop = get_default_shop()
    regular_person = get_person_contact(regular_user)
    product = get_default_product()

    wishlist = Wishlist.objects.create(shop=shop, customer=regular_person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(product)

    view_func = CustomerWishlistDetailView.as_view()
    request = apply_request_middleware(rf.get("/"), customer=regular_person)
    response = view_func(request, pk=wishlist.pk)

    assert response.status_code == 200
    assert 'customer_wishlist' in response.context_data
    assert response.context_data['customer_wishlist'].name == wishlist.name
    assert response.context_data['customer_wishlist'].products.count() == 1


@pytest.mark.django_db
def test_view_shared_wishlist_detail(rf, admin_user, regular_user):
    shop = get_default_shop()
    admin_person = get_person_contact(admin_user)
    regular_person = get_person_contact(regular_user)
    product = get_default_product()

    wishlist = Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.SHARED)
    wishlist.products.add(product)

    view_func = CustomerWishlistDetailView.as_view()
    request = apply_request_middleware(rf.get("/"), customer=regular_person)
    response = view_func(request, pk=wishlist.pk)

    assert response.status_code == 200
    assert 'customer_wishlist' in response.context_data
    assert response.context_data['customer_wishlist'].name == wishlist.name
    assert response.context_data['customer_wishlist'].products.count() == 1


@pytest.mark.django_db
def test_view_private_wishlist_detail(rf, admin_user, regular_user):
    shop = get_default_shop()
    admin_person = get_person_contact(admin_user)
    regular_person = get_person_contact(regular_user)
    product = get_default_product()

    wishlist = Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PRIVATE)
    wishlist.products.add(product)

    view_func = CustomerWishlistDetailView.as_view()
    request = apply_request_middleware(rf.get("/"), customer=regular_person)

    with pytest.raises(Http404):
        view_func(request, pk=wishlist.pk)


@pytest.mark.django_db
def test_delete_own_wishlist(rf, regular_user):
    shop = get_default_shop()
    person = get_person_contact(regular_user)
    product = get_default_product()

    wishlist = Wishlist.objects.create(shop=shop, customer=person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(product)

    view_func = WishlistDelete.as_view()
    request = apply_request_middleware(rf.post("/"), customer=person)
    response = view_func(request, pk=wishlist.pk)

    assert response.status_code == 302
    with pytest.raises(Wishlist.DoesNotExist):
        Wishlist.objects.get(pk=wishlist.pk)


@pytest.mark.django_db
def test_delete_other_persons_wishlist(rf, admin_user, regular_user):
    shop = get_default_shop()
    admin_person = get_person_contact(admin_user)
    person = get_person_contact(regular_user)
    product = get_default_product()

    wishlist = Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(product)

    view_func = WishlistDelete.as_view()
    request = apply_request_middleware(rf.post("/"), customer=person)
    with pytest.raises(Http404):
        view_func(request, pk=wishlist.pk)
    assert Wishlist.objects.filter(pk=wishlist.pk).exists()


@pytest.mark.django_db
def test_delete_own_wishlist_product(rf, regular_user):
    shop = get_default_shop()
    person = get_person_contact(regular_user)
    product = get_default_product()

    wishlist = Wishlist.objects.create(shop=shop, customer=person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(product)

    view_func = WishlistProductDelete.as_view()
    request = apply_request_middleware(rf.post("/"), customer=person)
    response = view_func(request, pk=wishlist.pk, product_pk=product.pk)

    assert response.status_code == 302
    with pytest.raises(ObjectDoesNotExist):
        Wishlist.objects.get(pk=wishlist.pk).products.get(pk=product.pk)


@pytest.mark.django_db
def test_delete_other_persons_wishlist_product(rf, admin_user, regular_user):
    shop = get_default_shop()
    admin_person = get_person_contact(admin_user)
    person = get_person_contact(regular_user)
    product = get_default_product()

    wishlist = Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(product)

    view_func = WishlistProductDelete.as_view()
    request = apply_request_middleware(rf.post("/"), customer=person)

    with pytest.raises(Http404):
        view_func(request, pk=wishlist.pk, product_pk=product.pk)
    assert Wishlist.objects.get(pk=wishlist.pk).products.filter(pk=product.pk).exists()
