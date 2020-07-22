# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from shuup_workbench.settings.utils import get_disabled_migrations
from shuup_workbench.test_settings import *  # noqa

INSTALLED_APPS = list(locals().get('INSTALLED_APPS', [])) + [
    'shuup_wishlist',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite3'
    }
}

MIGRATION_MODULES = get_disabled_migrations()
MIGRATION_MODULES.update({
    app: None
    for app in INSTALLED_APPS
})
