# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


@python_2_unicode_compatible
class Manufacturer(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    def __str__(self):
        return self.name


class CountryOfOrigin(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_('Country of origin'),
                              max_length=50,
                              blank=True)
    )

    class Meta:
        verbose_name = _('Country of origin')
        verbose_name_plural = _('Countries of origin')

    def __str__(self):
        return self.name
