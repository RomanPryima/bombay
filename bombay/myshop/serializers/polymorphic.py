# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.fields import empty

from shop.serializers.bases import ProductSerializer
from shop.serializers.defaults import AddToCartSerializer

from myshop.models import Clothes, SmartCard, SmartPhoneModel


class SmartCardSerializer(ProductSerializer):
    class Meta:
        model = SmartCard
        fields = ['product_name', 'slug', 'unit_price', 'manufacturer', 'card_type', 'speed',
                  'product_code', 'storage']


class SmartPhoneSerializer(ProductSerializer):
    class Meta:
        model = SmartPhoneModel
        fields = ['product_name', 'slug', 'battery_type', 'battery_capacity']


class ClothesSerializer(ProductSerializer):
    class Meta:
        model = Clothes
        fields = ['product_name', 'product_code', 'slug', 'size']


class AddSmartPhoneToCartSerializer(AddToCartSerializer):
    """
    Modified AddToCartSerializer which handles SmartPhones
    """
    def get_instance(self, context, data, extra_args):
        product = context['product']
        if data is empty:
            product_code = None
            extra = {}
        else:
            product_code = data.get('product_code')
            extra = data.get('extra', {})
        try:
            variant = product.get_product_variant(product_code=product_code)
        except product.DoesNotExist:
            variant = product.variants.first()
        extra.update(storage=variant.storage)
        instance = {
            'product': product.id,
            'product_code': variant.product_code,
            'unit_price': variant.unit_price,
            'extra': extra,
        }
        return instance


class AddClothesToCartSerializer(AddToCartSerializer):
    """
    Modified AddToCartSerializer which handles Clothes
    """

    product_size = serializers.CharField(read_only=True, help_text="Exact product csize of the cart item")

    def get_instance(self, context, data, extra_args):
        product = context['product']
        if data is empty:
            product_size = None
            extra = {}
        else:
            product_size = data.get('product_size')
            extra = data.get('extra', {})
        try:
            variant = product.get_product_variant(product_size=product_size)
        except product.DoesNotExist:
            variant = product.variants.first()
        extra.update(product_size=variant.product_size)
        instance = {
            'product': product.id,
            'product_size': variant.product_size,
            'product_code': product.product_code,
            'unit_price': product.unit_price,
            'extra': extra,
        }
        return instance
