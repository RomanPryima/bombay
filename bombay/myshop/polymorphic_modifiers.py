# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import FieldError

from shop.modifiers.defaults import DefaultCartModifier


class MyShopCartModifier(DefaultCartModifier):
    """
    Extended default cart modifier which handles the price for product variations
    """
    def process_cart_item(self, cart_item, request):
        try:
            variant = cart_item.product.get_product_variant(product_size= cart_item.extra.get('product_size'))
        except FieldError:
            variant = cart_item.product.get_product_variant(product_code=cart_item.product_code)
        try:
            cart_item.unit_price = variant.product.unit_price
        except AttributeError:
            cart_item.unit_price = variant.unit_price
        cart_item.line_total = cart_item.unit_price * cart_item.quantity
        # grandparent super
        return super(DefaultCartModifier, self).process_cart_item(cart_item, request)
