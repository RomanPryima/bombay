# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from shop.money.fields import MoneyField
from parler.managers import TranslatableManager
from parler.models import TranslatedFields
from .product import Product

GENDERS = (('m', _('Men')), ('w', _('Women')))
SEASONS = (
    ('spring-summer-fall', _('Spring, Summer, Fall')),
    ('winter', _('Winter')),
    ('whole_year', _('Whole year')),
)

SIZES = [(_, _) for _ in range(40, 69, 2)]


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
    season = models.CharField(_('Seson'), max_length=30, choices=SEASONS)

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
            int(round((self.price_without_discount.__float__() - self.unit_price.__float__()) /
                      self.unit_price.__float__() * 100, 0)))

    class Meta:
        verbose_name = _("Clothes")
        verbose_name_plural = _("Clothes")

    def get_price(self, request):
        return self.unit_price

    def is_in_cart(self, cart, watched=False, **kwargs):
        from shop.models.cart import CartItemModel
        try:
            product_code = kwargs['product_code']
            product_size = kwargs['extra']['product_size']
        except KeyError:
            return
        cart_item_qs = CartItemModel.objects.filter(cart=cart, product=self)
        for cart_item in cart_item_qs:
            if cart_item.product_code == product_code and cart_item.extra.get('product_size') ==  product_size:
                return cart_item

    def get_product_variant(self, **kwargs):
        try:
            return self.variants.get(**kwargs)
        except ClothesVariant.DoesNotExist as e:
            raise Clothes.DoesNotExist(e)

    @property
    def size_range(self):
        variants = self.variants.all()
        sizes = [variant.product_size for variant in variants]
        return '{} - {}'.format(min(sizes), max(sizes))


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


class UniversalClothes(Product):
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
    season = models.CharField(_('Seson'), max_length=30, choices=SEASONS)

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
            int(round((self.price_without_discount.__float__() - self.unit_price.__float__()) /
                      self.unit_price.__float__() * 100, 0)))

    class Meta:
        verbose_name = _("Universal Clothes")
        verbose_name_plural = _("Universal Clothes")

    def get_price(self, request):
        return self.unit_price

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

