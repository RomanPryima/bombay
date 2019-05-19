""" Command for easy cache clear. """
from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            caches['compressor'].clear()
            self.stdout.write('Cleared cache\n')
        except InvalidCacheBackendError:
            self.stdout.write('Cleaning cache failed\n')
