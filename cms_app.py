# -*- coding: utf8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class UserFormsHook(CMSApp):
    """ User Forms """
    name = "User Forms"
    urls = ["userforms.urls"]

apphook_pool.register(UserFormsHook)
