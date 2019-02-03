# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from shop.money import Money, MoneyMaker
from djangocms_text_ckeditor.fields import HTMLField
from shop.money.fields import MoneyField
from parler.managers import TranslatableManager
from parler.models import TranslatedFields
from .product import Product


class Clothes(Product):
    # common product fields
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

    multilingual = TranslatedFields(
        description=HTMLField(
            verbose_name=_("Description"),
            configuration='CKEDITOR_SETTINGS_DESCRIPTION',
            help_text=_("Full description used in the catalog's detail view of Clothes."),
        ),
        color=models.CharField(verbose_name=_('Color of product'), help_text=_('Color of product'), max_length=255,
                               null=True, blank=True),
        sezon=models.CharField(verbose_name=_('Product season'), help_text=_('Product season'), max_length=255,
                               null=True, blank=True),
        fabric=models.CharField(verbose_name=_('Fabric of product'), help_text=_('Fabric of product'), max_length=255,
                                null=True, blank=True),
        composition=models.CharField(verbose_name=_('Composition of product material'),
                                     help_text=_('Composition of product material'), max_length=255, null=True,
                                     blank=True),
        decoration=models.CharField(verbose_name=_('Decoration and features'),
                                    help_text=_('Decoration and features'), max_length=255, null=True, blank=True),
        condition=models.CharField(choices=[('new', _('New')), ('used', _('Used'))],
                                   verbose_name=_('Condition of product'), help_text=_('Condition of product'),
                                   max_length=255, null=True, blank=True)
    )

    default_manager = TranslatableManager()

    class Meta:
        verbose_name = _("Clothes (singular)")
        verbose_name_plural = _("Clothes")

    def get_price(self, request):
        return self.unit_price
