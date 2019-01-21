# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from shop.admin.defaults import customer
from shop.admin.defaults.order import OrderAdmin
from shop.models.defaults.order import Order
from shop.admin.order import PrintOrderAdminMixin
from shop.admin.delivery import DeliveryOrderAdminMixin
from . import bombay, manufacturer


class OrderAdmin(PrintOrderAdminMixin, DeliveryOrderAdminMixin, OrderAdmin):
    pass


admin.site.register(Order, OrderAdmin)

__all__ = ['commodity', 'customer']

admin.site.site_header = "Bombay-SHOP administration"
