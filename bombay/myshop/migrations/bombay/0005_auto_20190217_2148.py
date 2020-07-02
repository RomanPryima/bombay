# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-17 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0004_auto_20190217_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothestranslation',
            name='condition',
        ),
        migrations.AddField(
            model_name='clothes',
            name='condition',
            field=models.CharField(blank=True, choices=[('new', 'New'), ('used', 'Used')], help_text='Condition of product', max_length=255, null=True, verbose_name='Condition of product'),
        ),
    ]