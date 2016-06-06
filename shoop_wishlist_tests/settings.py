# -*- coding: utf-8 -*-
# This file is part of Shoop Wishlist.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import os
import tempfile

SECRET_KEY = "xxx"


INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "easy_thumbnails",
    "filer",
    "shoop.core",
    "shoop.front",
    "shoop.customer_group_pricing",
    "shoop.default_tax",
    "shoop.simple_cms",
    "shoop.xtheme",
    "shoop_wishlist",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(
            tempfile.gettempdir(),
            'shoop_stripe_tests.sqlite3'
        ),
    }
}


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


MIGRATION_MODULES = DisableMigrations()
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "var", "media")

STATIC_URL = "static/"

ROOT_URLCONF = 'shoop_workbench.urls'

LANGUAGES = [
    ('en', 'English'),
    ('fi', 'Finnish'),
    ('ja', 'Japanese'),
]

PARLER_DEFAULT_LANGUAGE_CODE = "en"

PARLER_LANGUAGES = {
    None: [{"code": c, "name": n} for (c, n) in LANGUAGES],
    'default': {
        'hide_untranslated': False,
    }
}

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja",
            "newstyle_gettext": True,
        },
        "NAME": "jinja2",
    },
]
