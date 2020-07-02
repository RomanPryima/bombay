# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-12 15:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('myshop', '0010_auto_20190312_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothes',
            name='condition',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='salutation',
        ),
        migrations.AddField(
            model_name='product',
            name='title_image',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.FILER_IMAGE_MODEL),
        ),
    ]