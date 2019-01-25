# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin

from myshop.models.manufacturer import Manufacturer, CountryOfOrigin


admin.site.register(Manufacturer, admin.ModelAdmin)


@admin.register(CountryOfOrigin)
class CountryOfOriginAdmin(TranslatableAdmin):
    base_model = CountryOfOrigin
    fieldsets = [
        (_("Translatable Fields"), {
            'fields': ['name'],
        })
    ]
