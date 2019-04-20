# -*- coding:utf-8 -*-
from django.conf import settings

from expense_management import settings as et_settings


def common_values(request):
    return {
        'ET': et_settings,

    }
