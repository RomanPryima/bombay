# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField

from filer.fields import image
from parler.models import TranslatableModelMixin, TranslatedFieldsModel
from parler.fields import TranslatedField
from parler.managers import TranslatableManager, TranslatableQuerySet
from polymorphic.query import PolymorphicQuerySet
from shop.models.product import BaseProductManager, BaseProduct, CMSPageReferenceMixin
from shop.models.categories import Category
from shop.models.defaults.mapping import ProductPage, ProductImage
from ..manufacturer import CountryOfOrigin, Manufacturer


AVAILABILITY = (
    ('available', _('Available')),
    ('not_available', _('Not available')),
    ('on_order', _('On Order')),
    ('avaiting_delivery', _('Avaiting Delivery')),
)

PROMO_OPTIONS = (
    ('best_seller', _('Best Seller')),
    ('sale', _('Sale')),
    ('new_product', _('New Product')),
    ('best_price', _('Best Price')),
)

class ProductQuerySet(TranslatableQuerySet, PolymorphicQuerySet):
    pass


class ProductManager(BaseProductManager, TranslatableManager):
    queryset_class = ProductQuerySet

    def get_queryset(self):
        qs = self.queryset_class(self.model, using=self._db)
        return qs.prefetch_related('translations')


@python_2_unicode_compatible
class Product(CMSPageReferenceMixin, TranslatableModelMixin, BaseProduct):
    """
    Base class to describe a polymorphic product. Here we declare common fields available in all of
    our different product types. These common fields are also used to build up the view displaying
    a list of all products.
    """
    product_name = TranslatedField()

    availability = models.CharField(
        _('Availability'),
        max_length=50,
        choices=AVAILABILITY
    )

    promo_option = models.CharField(
        _('Promo option'),
        max_length=50,
        choices=PROMO_OPTIONS,
        null=True, blank=True,
    )

    slug = models.SlugField(
        _("Slug"),
        unique=True,
    )

    caption = TranslatedField()

    # common product properties
    manufacturer = models.ForeignKey(
        Manufacturer,
        verbose_name=_("Manufacturer"),
        null=True, blank=True
    )

    country_of_origin = models.ForeignKey(
        CountryOfOrigin,
        verbose_name=_("Country of origin"),
        null=True, blank=True
    )

    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        null=True,  blank=True
    )

    # controlling the catalog
    order = models.PositiveIntegerField(
        _("Sort by"),
        db_index=True,
    )

    cms_pages = models.ManyToManyField(
        'cms.Page',
        through=ProductPage,
        help_text=_("Choose list view this product shall appear on."),
    )

    images = models.ManyToManyField(
        'filer.Image',
        through=ProductImage,
    )

    title_image = image.FilerImageField(
        related_name='+',
        blank=True, null=True
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    objects = ProductManager()

    # filter expression used to lookup for a product item using the Select2 widget
    lookup_fields = ('product_name__icontains',)

    def __str__(self):
        return self.product_name

    @property
    def sample_image(self):
        return self.title_image


class ProductTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(
        Product,
        related_name='translations',
        null=True,
    )

    product_name = models.CharField(
        _("Product Name"),
        max_length=255,
    )

    caption = HTMLField(
        verbose_name=_("Caption"),
        blank=True,
        null=True,
        configuration='CKEDITOR_SETTINGS_CAPTION',
        help_text=_("Short description used in the catalog's list view of products."),
    )

    class Meta:
        unique_together = [('language_code', 'master')]
