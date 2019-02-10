from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin

from ..models.categories import Category


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    base_model = Category
    fieldsets = [
        (_("Translatable Fields"), {
            'fields': ['name', 'slug', 'image', 'page'],
        })
    ]
