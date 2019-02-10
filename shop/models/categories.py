# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pagemodel import Page
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_('Product category'),
                              max_length=50,
                              blank=True)
    )

    page = models.ForeignKey(Page, null=True, blank=True)

    slug = models.SlugField(_('Slug'))

    image = FilerImageField(null=True, blank=True,
                           related_name="category_image")

    class Meta:
        verbose_name = _('Product catgory')
        verbose_name_plural = _('Product catgories')

    def __str__(self):
        return self.name
