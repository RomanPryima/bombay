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


class ClothesModel(Product):
    """
    A generic clothes model, which must be concretized by a model `Dresses` - see below.
    """

    multilingual = TranslatedFields(
        description=HTMLField(
            verbose_name=_("Description"),
            configuration='CKEDITOR_SETTINGS_DESCRIPTION',
            help_text=_("Full description used in the catalog's detail view of Dresses."),
        ),
    )
    product_code = models.CharField(
        _("Product code"),
        max_length=255,
        unique=True,
    )

    size = models.CharField(
        _("Available sizes"),
        max_length=50,
        help_text=_("Available sizes of the item"),
    )

    default_manager = TranslatableManager()

    class Meta:
        verbose_name = _("Clothes")
        verbose_name_plural = _("Clothes")

    def get_price(self, request):
        """
        Return the starting price for instances of this smart phone model.
        """
        if not hasattr(self, '_price'):
            if self.variants.exists():
                currency = self.variants.first().unit_price.currency
                aggr = self.variants.aggregate(models.Min('unit_price'))
                self._price = MoneyMaker(currency)(aggr['unit_price__min'])
            else:
                self._price = Money()
        return self._price

    def is_in_cart(self, cart, watched=False, **kwargs):
        from shop.models.cart import CartItemModel
        try:
            product_code = kwargs['product_code']
        except KeyError:
            return
        cart_item_qs = CartItemModel.objects.filter(cart=cart, product=self)
        for cart_item in cart_item_qs:
            if cart_item.product_code == product_code:
                return cart_item

    def get_product_variant(self, **kwargs):
        try:
            return self.variants.get(**kwargs)
        except ClothesVariant.DoesNotExist as e:
            raise ClothesVariant.DoesNotExist(e)


class ClothesVariant(models.Model):
    product = models.ForeignKey(
        ClothesModel,
        verbose_name=_("Clothes Model"),
        related_name='variants',
    )

    unit_price = MoneyField(
        _("Unit price"),
        decimal_places=2,
        help_text=_("Net price for this product"),
    )

    colour = models.CharField(
        _("Color"),
        max_length=50,
        help_text=_("Color of the item"),
    )

    def get_price(self, request):
        return self.unit_price
