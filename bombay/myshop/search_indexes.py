# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from haystack import indexes
from shop.search.indexes import ProductIndex as ProductIndexBase
from myshop.models import  Commodity, Clothes, UniversalClothes


class ProductIndex(ProductIndexBase):
    catalog_media = indexes.CharField(stored=True, indexed=False, null=True)
    search_media = indexes.CharField(stored=True, indexed=False, null=True)
    caption = indexes.CharField(stored=True, indexed=False, null=True, model_attr='caption')

    def prepare_catalog_media(self, product):
        return self.render_html('catalog', product, 'media')

    def prepare_search_media(self, product):
        return self.render_html('search', product, 'media')


myshop_search_index_classes = []

class CommodityIndex(ProductIndex, indexes.Indexable):
    def get_model(self):
        return Commodity
myshop_search_index_classes.append(CommodityIndex)

class UniversalClothesIndex(ProductIndex, indexes.Indexable):
    def get_model(self):
        return UniversalClothes
myshop_search_index_classes.append(UniversalClothesIndex)

class ClothesIndex(ProductIndex, indexes.Indexable):
    def get_model(self):
        return Clothes
myshop_search_index_classes.append(ClothesIndex)

