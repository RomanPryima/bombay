# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Max
from django.template.context import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from adminsortable2.admin import SortableAdminMixin, PolymorphicSortableAdminMixin

from cms.admin.placeholderadmin import PlaceholderAdminMixin, FrontendEditableAdminMixin
from parler.admin import TranslatableAdmin
from polymorphic.admin import (PolymorphicParentModelAdmin, PolymorphicChildModelAdmin,
                               PolymorphicChildModelFilter)

from shop.admin.product import CMSPageAsCategoryMixin, ProductImageInline, InvalidateProductCacheMixin, CMSPageFilter

from myshop.models import Product, Commodity, Clothes, ClothesVariant, UniversalClothes
# from myshop.models.bombay.smartphone import OperatingSystem


@admin.register(Commodity)
class CommodityAdmin(InvalidateProductCacheMixin, SortableAdminMixin, TranslatableAdmin, FrontendEditableAdminMixin,
                     PlaceholderAdminMixin, CMSPageAsCategoryMixin, admin.ModelAdmin):
    """
    Since our Commodity model inherits from polymorphic Product, we have to redefine its admin class.
    """
    base_model = Product
    fieldsets = [
        (None, {
            'fields': ['product_name', 'availability', 'category',
                       'slug', 'product_code', 'unit_price',
                       'price_without_discount', 'active', 'title_image'
                       ],
        }),
        (_("Translatable Fields"), {
            'fields': ['color', 'hair_type', 'classification', 'package', 'weight', 'caption', 'description'],
        }),
        (_("Properties"), {
            'fields': ['manufacturer', 'country_of_origin'],
        }),
    ]
    filter_horizontal = ['cms_pages']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ['product_code']}


@admin.register(UniversalClothes)
class UniversalClothesAdmin(InvalidateProductCacheMixin, SortableAdminMixin, TranslatableAdmin, FrontendEditableAdminMixin,
                     PlaceholderAdminMixin, CMSPageAsCategoryMixin, admin.ModelAdmin):
    base_model = Product
    fieldsets = [
        (None, {
            'fields': ['product_name',
                       'availability',
                       'promo_option',
                       'product_code',
                       'slug',
                       'price_without_discount',
                       'unit_price',
                       'active',
                       'country_of_origin',
                       'category',
                       'color',
                       'fabric',
                       'season',
                       'composition',
                       'decoration',
                       'manufacturer',
                       'gender',
                       'title_image',
                       ],
        }),
        (_("Translatable Fields"), {
            'fields': ['caption', 'description'],
        }),
    ]
    filter_horizontal = ['cms_pages']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ['product_code']}


class ClothesInline(admin.TabularInline):
    model = ClothesVariant
    min_num = 1
    extra = 0


@admin.register(Clothes)
class ClothesAdmin(InvalidateProductCacheMixin, SortableAdminMixin, TranslatableAdmin, FrontendEditableAdminMixin,
                     CMSPageAsCategoryMixin, PlaceholderAdminMixin, PolymorphicChildModelAdmin):
    base_model = Product
    fieldsets = [
        (None, {
            'fields': ['product_name',
                       'availability',
                       'promo_option',
                       'product_code',
                       'slug',
                       'price_without_discount',
                       'unit_price',
                       'active',
                       'country_of_origin',
                       'category',
                       'color',
                       'fabric',
                       'season',
                       'composition',
                       'decoration',
                       'manufacturer',
                       'gender',
                       'title_image',
                       ],
        }),
        (_("Translatable Fields"), {
            'fields': ['caption', 'description'],
        }),
    ]
    filter_horizontal = ['cms_pages']
    inlines = [ProductImageInline, ClothesInline]
    prepopulated_fields = {'slug': ['product_code']}


@admin.register(Product)
class ProductAdmin(PolymorphicSortableAdminMixin, PolymorphicParentModelAdmin):
    base_model = Product
    child_models = [Clothes, Commodity]
    list_display = ['product_name', 'get_price', 'product_type', 'active']
    list_display_links = ['product_name']
    search_fields = ['product_name']
    list_filter = [PolymorphicChildModelFilter, CMSPageFilter]
    list_per_page = 50
    list_max_show_all = 1000

    def get_price(self, obj):
        return str(obj.get_real_instance().get_price(None))
    get_price.short_description = _("Price")
