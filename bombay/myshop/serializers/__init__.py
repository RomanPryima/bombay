# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.safestring import mark_safe

from rest_framework import serializers

from shop.serializers.bases import ProductSerializer
from shop.search.serializers import ProductSearchSerializer as BaseProductSearchSerializer

from myshop.search_indexes import myshop_search_index_classes
from .polymorphic import (SmartCardSerializer, ClothesSerializer, AddClothesToCartSerializer)


__all__ = ['ProductSummarySerializer', 'ProductSearchSerializer', 'CatalogSearchSerializer',
           'SmartCardSerializer', 'ClothesSerializer', 'AddClothesToCartSerializer']


class ProductSummarySerializer(ProductSerializer):
    media = serializers.SerializerMethodField()
    size_range = serializers.CharField(max_length=30, allow_null=True, allow_blank=True)
    discount = serializers.CharField(max_length=10, allow_null=True, allow_blank=True)
    email_picture_url = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ['id', 'product_name', 'product_url', 'product_model', 'price', 'media', 'caption', 'size_range',
                  'price_without_discount', 'discount', 'email_picture_url']

    def get_media(self, product):
        return self.render_html(product, 'media')

    def get_size_range(self, product):
        return product.size_range

    def get_email_picture_url(self, product):
        return product.title_image.url


class ProductSearchSerializer(BaseProductSearchSerializer):
    """
    Serializer to search over all products in this shop
    """
    media = serializers.SerializerMethodField()

    class Meta(BaseProductSearchSerializer.Meta):
        fields = BaseProductSearchSerializer.Meta.fields + ['media', 'caption']
        field_aliases = {'q': 'text'}
        search_fields = ['text']
        index_classes = myshop_search_index_classes

    def get_media(self, search_result):
        return mark_safe(search_result.search_media)


class CatalogSearchSerializer(BaseProductSearchSerializer):
    """
    Serializer to restrict products in the catalog
    """
    media = serializers.SerializerMethodField()

    class Meta(BaseProductSearchSerializer.Meta):
        fields = BaseProductSearchSerializer.Meta.fields + ['media', 'caption']
        field_aliases = {'q': 'autocomplete'}
        search_fields = ['autocomplete']
        index_classes = myshop_search_index_classes

    def get_media(self, search_result):
        return mark_safe(search_result.catalog_media)
