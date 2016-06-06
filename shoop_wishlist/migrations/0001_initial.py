# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import shoop_wishlist.models


class Migration(migrations.Migration):

    dependencies = [
        ('shoop', '0025_add_codes_for_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('privacy', enumfields.fields.EnumIntegerField(default=2, enum=shoop_wishlist.models.WishlistPrivacy, verbose_name='privacy')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('customer', models.ForeignKey(verbose_name='customer', to='shoop.Contact')),
                ('products', models.ManyToManyField(related_name='wishlists', verbose_name='products', to='shoop.Product')),
                ('shop', models.ForeignKey(verbose_name='shop', to='shoop.Shop')),
            ],
            options={
                'verbose_name': 'Wishlist',
                'verbose_name_plural': 'Wishlists',
            },
        ),
    ]
