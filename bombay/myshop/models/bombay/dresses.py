# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from shop.money.fields import MoneyField
from parler.managers import TranslatableManager
from parler.models import TranslatedFields
from .product import Product

GENDERS = (('m', _('Men')), ('w', _('Women')))
SEASONS = (
    ('spring', _('Spring')),
    ('summer', _('Summer')),
    ('fall', _('Fall')),
    ('winter', _('Winter')),
)
SIZES = [(_, _) for _ in range(44, 68)]

class Clothes(Product):
    # common product fields
    unit_price = MoneyField(
        _("Unit price"),
        decimal_places=2,
        help_text=_("Net price for this product"),
    )

    price_without_discount = MoneyField(
        _("Price without discount"),
        decimal_places=2,
        help_text=_("Price for this product without applying a discount."),
    )

    product_code = models.CharField(
        _("Product code"),
        max_length=255,
        unique=True,
    )

    gender = models.CharField(_('Gender'), max_length=15, choices=GENDERS)
    season = models.CharField(_('Seson'), max_length=15, choices=SEASONS)

    condition = models.CharField(choices=[(_('new'), _('New')), (_('used'), _('Used'))],
                                 verbose_name=_('Condition of product'), help_text=_('Condition of product'),
                                 max_length=255, null=True, blank=True)

    multilingual = TranslatedFields(
        description=HTMLField(
            verbose_name=_("Description"),
            configuration='CKEDITOR_SETTINGS_DESCRIPTION',
            help_text=_("Full description used in the catalog's detail view of Clothes."),
        ),
        color=models.CharField(verbose_name=_('Color of product'), help_text=_('Color of product'), max_length=255,
                               null=True, blank=True),
        fabric=models.CharField(verbose_name=_('Fabric of product'), help_text=_('Fabric of product'), max_length=255,
                                null=True, blank=True),
        composition=models.CharField(verbose_name=_('Composition of product material'),
                                     help_text=_('Composition of product material'), max_length=255, null=True,
                                     blank=True),
        decoration=models.CharField(verbose_name=_('Decoration and features'),
                                    help_text=_('Decoration and features'), max_length=255, null=True, blank=True),
    )

    default_manager = TranslatableManager()

    @property
    def discount(self):
        return '- {} %'.format(
            str(round((self.price_without_discount.__float__() - self.unit_price.__float__()) /
                      self.unit_price.__float__() * 100, 0)))

    class Meta:
        verbose_name = _("Clothes")
        verbose_name_plural = _("Clothes")

    def get_price(self, request):
        return self.unit_price


class ClothesVariant(models.Model):
    product = models.ForeignKey(
        Clothes,
        verbose_name=_("Clothes name"),
        related_name='variants',
    )

    product_size = models.PositiveIntegerField(
        _("Product size"),
        help_text=_("Size of Item"),
        choices=SIZES
    )
