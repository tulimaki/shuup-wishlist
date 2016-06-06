# -*- coding: utf-8 -*-
# This file is part of Shoop Wishlist.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.db.models import Count, Q
from django.http import Http404
from django.http.response import HttpResponseRedirect, JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from shoop.core.models import Product
from shoop_wishlist.models import Wishlist, WishlistPrivacy


class CustomerWishlistsView(ListView):
    model = Wishlist
    context_object_name = 'customer_wishlists'
    template_name = 'shoop_wishlist/customer_wishlists.jinja'

    def get_queryset(self):
        qs = super(CustomerWishlistsView, self).get_queryset()
        return qs.filter(customer=self.request.customer).annotate(product_count=Count('products'))


class CustomerWishlistDetailView(DetailView):
    model = Wishlist
    context_object_name = 'customer_wishlist'
    template_name = 'shoop_wishlist/customer_wishlist_detail.jinja'

    def get_queryset(self):
        qs = super(CustomerWishlistDetailView, self).get_queryset()
        qs = qs.filter(Q(customer=self.request.customer) | Q(privacy=WishlistPrivacy.SHARED))
        return qs.prefetch_related('products').all()


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['name', 'privacy']

    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop', None)
        self.customer = kwargs.pop('customer', None)
        self.product_id = kwargs.pop('product_id', None)
        super(WishlistForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        if self.product_id:
            product = Product.objects.get(pk=self.product_id)
            shop_product = product.get_shop_instance(self.shop)
            errors = shop_product.get_visibility_errors(self.customer)
            for error in errors:
                self.add_error(None, error)
        return super(WishlistForm, self).is_valid()


class WishlistCreate(CreateView):
    form_class = WishlistForm
    template_name = 'shoop_wishlist/create_wishlist_modal.jinja'

    @transaction.atomic
    def form_valid(self, form):
        shop = self.request.shop
        customer = self.request.customer
        product_id = self.request.POST.get('product_id')
        response = {}
        wishlist, created = Wishlist.objects.get_or_create(shop=shop, customer=customer, **form.cleaned_data)
        response['id'] = wishlist.id
        response['name'] = wishlist.name
        if created and product_id:
            wishlist.products.add(product_id)
            response['product_name'] = wishlist.products.get(pk=product_id).name
        response['created'] = created
        return JsonResponse(response)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def get_form(self):
        kwargs = self.get_form_kwargs()
        kwargs['shop'] = self.request.shop
        kwargs['customer'] = self.request.customer
        kwargs['product_id'] = self.request.POST.get('product_id')
        return WishlistForm(**kwargs)

    def get_context_data(self, **kwargs):
        data = super(WishlistCreate, self).get_context_data(**kwargs)
        data['product_id'] = self.request.GET.get('product_id')
        return data


class WishlistDelete(DeleteView):
    model = Wishlist
    success_url = reverse_lazy('shoop:personal_wishlists')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.customer == request.customer:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            raise Http404


class WishlistProductDelete(DeleteView):
    model = Wishlist

    def delete(self, request, *args, **kwargs):
        wishlist = self.get_object()
        if wishlist.customer == request.customer:
            wishlist.products.remove(self.kwargs['product_pk'])
            return HttpResponseRedirect(reverse_lazy('shoop:wishlist_detail', kwargs=dict(pk=wishlist.pk)))
        else:
            raise Http404


def add_product_to_wishlist(request, wishlist_id, product_id):
    response = {'created': False}

    if request.method != 'POST':
        return JsonResponse({'err': 'invalid request'}, status=405)

    if not getattr(request, 'customer', None):
        return JsonResponse({'err': 'unauthorized request'}, status=403)

    # ensure wishlist belongs to currently logged in user
    wishlist = Wishlist.objects.filter(customer=request.customer, id=wishlist_id).first()
    if wishlist:
        created = not wishlist.products.filter(id=product_id).exists()
        response['created'] = created
        if created:
            wishlist.products.add(product_id)
        response['product_name'] = wishlist.products.get(id=product_id).name
    else:
        return JsonResponse({'err': 'invalid wishlist'}, status=400)
    return JsonResponse(response)
