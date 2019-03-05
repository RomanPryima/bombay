# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from cms.models.fields import PlaceholderField
from parler.managers import TranslatableManager
from parler.models import TranslatedFields
from shop.money.fields import MoneyField
from .product import Product


class Commodity(Product):
    """
    This Commodity model inherits from polymorphic Product, and therefore has to be redefined.
    """
    unit_price = MoneyField(
        _("Unit price"),
        decimal_places=3,
        help_text=_("Net price for this product"),
    )

    product_code = models.CharField(
        _("Product code"),
        max_length=255,
        unique=True,
    )

    price_without_discount = MoneyField(
        _("Price without discount"),
        decimal_places=2,
        help_text=_("Price for this product without applying a discount."),
    )

    # controlling the catalog
    placeholder = PlaceholderField("Commodity Details")
    show_breadcrumb = True  # hard coded to always show the product's breadcrumb


    multilingual = TranslatedFields(
        description=HTMLField(
            verbose_name=_("Description"),
            configuration='CKEDITOR_SETTINGS_DESCRIPTION',
            help_text=_("Full description used in the catalog's detail view of Commodity."),
        ),
        color=models.CharField(verbose_name=_('Color and shades of product'), help_text=_('Color and shades of product'),
                               max_length=255,
                               null=True, blank=True),
        hair_type=models.CharField(verbose_name=_('Type of hair'), help_text=_('Type of hair'), max_length=255,
                                null=True, blank=True),
        classification=models.CharField(verbose_name=_('Classification of the commodity'),
                                     help_text=_('Classification of the commodityl'), max_length=255, null=True,
                                     blank=True),
        package=models.CharField(verbose_name=_('Package'),
                                    help_text=_('Package'), max_length=255, null=True, blank=True),
        weight=models.CharField(verbose_name=_('Weight/Volume'),
                                 help_text=_('Weight/Volume'), max_length=100, null=True, blank=True),
    )

    default_manager = TranslatableManager()

    class Meta:
        verbose_name = _("Commodity")
        verbose_name_plural = _("Commodities")

    def get_price(self, request):
        return self.unit_price

    @property
    def discount(self):
        return '- {} %'.format(
            int(round((self.price_without_discount.__float__() - self.unit_price.__float__()) /
                      self.unit_price.__float__() * 100, 0)))
