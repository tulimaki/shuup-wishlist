# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
import json

import pytest
from django.core.urlresolvers import reverse
from django.db.models import ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import activate

from shuup.core.models import get_person_contact
from shuup.testing.factories import (
    create_product, get_default_product, get_default_shop,
    get_default_supplier, get_shop
)
from shuup.testing.utils import apply_request_middleware
from shuup_wishlist.models import Wishlist, WishlistPrivacy
from shuup_wishlist.views import (
    add_product_to_wishlist, WishlistCreateView, WishlistCustomerDetailView,
    WishlistCustomerView, WishlistDeleteView, WishlistProductDeleteView,
    WishlistSearchView
)

from .fixtures import regular_user

regular_user = regular_user  # noqa


def assert_wishlist(request, shop, person, view_func, product_count):
    request = apply_request_middleware(request, shop=shop, user=person.user)
    response = view_func(request)
    data = json.loads(response.content.decode("utf-8"))
    wishlist = Wishlist.objects.filter(shop=shop, customer=person).first()

    assert response.status_code == 200
    assert data.get('name', '') == 'foo'
    assert data.get('created', False)
    assert Wishlist.objects.filter(shop=shop, customer=person).count() == 1
    assert str(wishlist) == wishlist.name
    assert wishlist.name == 'foo'
    assert wishlist.privacy == WishlistPrivacy.PUBLIC
    assert wishlist.products.count() == product_count


@pytest.mark.django_db
def test_wishlist_create_invalid(admin_user, rf):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    view_func = WishlistCreateView.as_view()
    request = apply_request_middleware(rf.post("/"), shop=shop, user=person.user)
    response = view_func(request)

    assert response.status_code == 400


@pytest.mark.django_db
def test_wishlist_create(admin_user, rf):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    view_func = WishlistCreateView.as_view()
    request = rf.post("/", {"name": "foo", "privacy": 0})
    assert_wishlist(request, shop, person, view_func, 0)


@pytest.mark.django_db
def test_wishlist_create_with_product(admin_user, rf):
    activate("en")
    shop1 = get_shop(identifier="shop1", domain="shop1", name="shop1")
    shop2 = get_shop(identifier="shop2", domain="shop2", name="shop2")

    person = get_person_contact(admin_user)

    create_product("p1_s1", shop1, get_default_supplier())
    create_product("p1_s2", shop2, get_default_supplier())
    product2_s1 = create_product("p2_s1", shop1, get_default_supplier())
    product2_s2 = create_product("p2_s2", shop2, get_default_supplier())

    shop1_product2 = product2_s1.get_shop_instance(shop1)
    view_func = WishlistCreateView.as_view()
    request = rf.post("/", {"name": "foo", "privacy": 0, "shop_product_id": shop1_product2.id}, HTTP_HOST=shop1.domain)
    assert_wishlist(request, shop1, person, view_func, 1)

    shop2_product2 = product2_s2.get_shop_instance(shop2)
    request = rf.post("/", {"name": "foo", "privacy": 0, "shop_product_id": shop2_product2.id}, HTTP_HOST=shop2.domain)
    assert_wishlist(request, shop2, person, view_func, 1)


@pytest.mark.django_db
def test_wishlist_create_with_deleted_product(admin_user, rf):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    product = get_default_product()
    product.soft_delete(admin_user)
    shop_product = product.get_shop_instance(shop)
    view_func = WishlistCreateView.as_view()
    request = rf.post("/", {"name": "foo", "privacy": 0, "shop_product_id": shop_product.id})
    request = apply_request_middleware(request, shop=shop, user=person.user)
    response = view_func(request)

    assert response.status_code == 400


@pytest.mark.django_db
def test_wishlist_create_get_context_data(admin_user, rf):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    view_func = WishlistCreateView.as_view()
    request = apply_request_middleware(rf.get("/?shop_product_id=1"), shop=shop, user=person.user)
    response = view_func(request)

    assert response.status_code == 200
    assert 'shop_product_id' in response.context_data.keys()
    assert response.context_data.get('shop_product_id') == '1'


@pytest.mark.django_db
def test_add_product_to_wishlist_invalid_method(rf):
    get_default_shop()
    request = apply_request_middleware(rf.get("/"))
    response = add_product_to_wishlist(request, 0, 0)

    assert response.status_code == 405


@pytest.mark.django_db
def test_add_product_to_wishlist_unauthorized(rf, admin_user, regular_user):
    shop = get_default_shop()
    request = apply_request_middleware(rf.post("/"))
    response = add_product_to_wishlist(request, 0, 0)

    assert response.status_code == 403

    shop = get_default_shop()
    person = get_person_contact(regular_user)
    product = get_default_product()
    shop_product = product.get_shop_instance(shop)
    other_person = get_person_contact(admin_user)
    wishlist = Wishlist.objects.create(shop=shop, customer=other_person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    request = apply_request_middleware(rf.post("/"), user=person.user)
    assert request.customer
    response = add_product_to_wishlist(request, wishlist.id, shop_product.id)
    assert response.status_code == 400


@pytest.mark.django_db
def test_add_product_to_wishlist(rf, admin_user):
    shop = get_default_shop()
    person = get_person_contact(admin_user)
    product = get_default_product()
    shop_product = product.get_shop_instance(shop)
    wishlist = Wishlist.objects.create(shop=shop, customer=person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    request = apply_request_middleware(rf.post("/"), user=person.user)
    response = add_product_to_wishlist(request, wishlist.id, shop_product.id)
    data = json.loads(response.content.decode("utf-8"))

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
    shop_product = product.get_shop_instance(shop)

    wishlist = Wishlist.objects.create(shop=shop, customer=person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(shop_product)
    Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PUBLIC)

    view_func = WishlistCustomerView.as_view()
    request = apply_request_middleware(rf.get("/"), user=person.user)
    response = view_func(request)

    assert response.status_code == 200
    assert 'customer_wishlists' in response.context_data
    assert response.context_data['customer_wishlists'].count() == 1


@pytest.mark.django_db
def test_view_own_wishlist_detail(rf, regular_user):
    shop = get_default_shop()
    regular_person = get_person_contact(regular_user)
    product = get_default_product()
    shop_product = product.get_shop_instance(shop)

    wishlist = Wishlist.objects.create(shop=shop, customer=regular_person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(shop_product)

    view_func = WishlistCustomerDetailView.as_view()
    request = apply_request_middleware(rf.get("/"), user=regular_person.user)
    response = view_func(request, pk=wishlist.pk)

    assert response.status_code == 200
    assert 'customer_wishlist' in response.context_data
    assert response.context_data["is_owner"]
    assert response.context_data['customer_wishlist'].name == wishlist.name
    assert response.context_data['customer_wishlist'].products.count() == 1


@pytest.mark.parametrize("is_anonymous", [
    True, False
])
@pytest.mark.django_db
def test_view_shared_wishlist_detail(rf, admin_user, regular_user, is_anonymous):
    shop = get_default_shop()
    admin_person = get_person_contact(admin_user)
    regular_person = get_person_contact(regular_user)
    product = get_default_product()
    shop_product = product.get_shop_instance(shop)

    wishlist = Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.SHARED)
    wishlist.products.add(shop_product)
    view_func = WishlistCustomerDetailView.as_view()

    if(is_anonymous):
        request = apply_request_middleware(rf.get("/"))
        assert request.customer.pk is None
        response = view_func(request, pk=wishlist.pk)
        assert response.status_code == 302
        assert response.url.endswith(reverse('shuup:index'))
    else:
        request = apply_request_middleware(rf.get("/"), user=regular_person.user)
        response = view_func(request, pk=wishlist.pk)
        assert response.status_code == 200
        assert 'customer_wishlist' in response.context_data
        assert not response.context_data["is_owner"]
        assert response.context_data['customer_wishlist'].name == wishlist.name
        assert response.context_data['customer_wishlist'].products.count() == 1


@pytest.mark.django_db
def test_view_private_wishlist_detail(rf, admin_user, regular_user):
    shop = get_default_shop()
    admin_person = get_person_contact(admin_user)
    regular_person = get_person_contact(regular_user)
    product = get_default_product()
    shop_product = product.get_shop_instance(shop)

    wishlist = Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PRIVATE)
    wishlist.products.add(shop_product)

    view_func = WishlistCustomerDetailView.as_view()
    request = apply_request_middleware(rf.get("/"), user=regular_person.user)

    with pytest.raises(Http404):
        view_func(request, pk=wishlist.pk)


@pytest.mark.django_db
def test_delete_own_wishlist(rf, regular_user):
    shop = get_default_shop()
    person = get_person_contact(regular_user)
    product = get_default_product()
    shop_product = product.get_shop_instance(shop)

    wishlist = Wishlist.objects.create(shop=shop, customer=person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(shop_product)

    view_func = WishlistDeleteView.as_view()
    request = apply_request_middleware(rf.post("/"), user=person.user)
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
    shop_product = product.get_shop_instance(shop)

    wishlist = Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(shop_product)

    view_func = WishlistDeleteView.as_view()
    request = apply_request_middleware(rf.post("/"), user=person.user)
    with pytest.raises(Http404):
        view_func(request, pk=wishlist.pk)
    assert Wishlist.objects.filter(pk=wishlist.pk).exists()


@pytest.mark.django_db
def test_delete_own_wishlist_product(rf, regular_user):
    shop = get_default_shop()
    person = get_person_contact(regular_user)
    product = get_default_product()
    shop_product = product.get_shop_instance(shop)

    wishlist = Wishlist.objects.create(shop=shop, customer=person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(shop_product)

    view_func = WishlistProductDeleteView.as_view()
    request = apply_request_middleware(rf.post("/"), user=person.user)
    response = view_func(request, pk=wishlist.pk, shop_product_pk=shop_product.pk)

    assert response.status_code == 302
    with pytest.raises(ObjectDoesNotExist):
        Wishlist.objects.get(pk=wishlist.pk).products.get(pk=shop_product.pk)


@pytest.mark.django_db
def test_delete_other_persons_wishlist_product(rf, admin_user, regular_user):
    shop = get_default_shop()
    admin_person = get_person_contact(admin_user)
    person = get_person_contact(regular_user)
    product = get_default_product()
    shop_product = product.get_shop_instance(shop)

    wishlist = Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    wishlist.products.add(shop_product)

    view_func = WishlistProductDeleteView.as_view()
    request = apply_request_middleware(rf.post("/"), user=person.user)

    with pytest.raises(Http404):
        view_func(request, pk=wishlist.pk, shop_product_pk=shop_product.pk)
    assert Wishlist.objects.get(pk=wishlist.pk).products.filter(pk=shop_product.pk).exists()


@pytest.mark.django_db
def test_wishlist_search(rf, admin_user, regular_user):
    shop = get_default_shop()
    admin_person = get_person_contact(admin_user)
    person = get_person_contact(regular_user)

    Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PUBLIC)
    Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.SHARED)
    Wishlist.objects.create(shop=shop, customer=admin_person, name='foo', privacy=WishlistPrivacy.PRIVATE)

    view_func = WishlistSearchView.as_view()

    request = apply_request_middleware(rf.get("/?q=foo"), user=person.user)
    response = view_func(request)

    assert response.status_code == 200
    assert len(response.context_data["wishlists"]) == 1
