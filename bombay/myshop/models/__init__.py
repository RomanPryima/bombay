# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import default models from shop to materialize them
from shop.models.defaults.address import ShippingAddress, BillingAddress
from shop.models.defaults.cart import Cart
from shop.models.defaults.cart_item import CartItem
from shop.models.defaults.customer import Customer

__all__ = ['ShippingAddress', 'BillingAddress', 'Cart', 'CartItem', 'Customer', 'OrderItem',
           'Commodity', 'SmartCard', 'SmartPhoneModel', 'SmartPhoneVariant', 'Delivery', 'DeliveryItem']

from .bombay.order import OrderItem
from .bombay.product import Product
from .bombay.commodity import Commodity
from .bombay.smartcard import SmartCard
from .bombay.smartphone import SmartPhoneModel, SmartPhoneVariant
from shop.models.defaults.delivery import Delivery, DeliveryItem
