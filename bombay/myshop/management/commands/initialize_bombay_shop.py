# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
try:
    import czipfile as zipfile
except ImportError:
    import zipfile


class Command(BaseCommand):
    version = 13
    help = _("Initialize the workdir to run the bombay myshop.")
    download_url = 'http://downloads.django-shop.org/django-shop-workdir_i18n_polymorphic-{version}.zip'
    pwd = b'z7xv'

    def add_arguments(self, parser):
        parser.add_argument('--noinput', '--no-input', action='store_false', dest='interactive',
                            default=True, help="Do NOT prompt the user for input of any kind.")

    def set_options(self, **options):
        self.interactive = options['interactive']

    def createdb_if_not_exists(self):
        try:
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        except ImportError:
            return

        dbname = os.getenv('POSTGRES_DB')
        if dbname is None:
            return
        host = os.getenv('POSTGRES_HOST')
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        try:
            con = psycopg2.connect(dbname=dbname, host=host, user=user, password=password)
        except psycopg2.OperationalError:
            con = psycopg2.connect(host=host, user=user, password=password)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            cur.execute('CREATE DATABASE {};'.format(dbname))
        finally:
            con.close()

    def clear_compressor_cache(self):
        from django.core.cache import caches
        from django.core.cache.backends.base import InvalidCacheBackendError
        from compressor.conf import settings as s

        cache_dir = os.path.join(s.STATIC_ROOT, s.COMPRESS_OUTPUT_DIR)
        if settings.COMPRESS_ENABLED is False or os.listdir(cache_dir) != []:
            return
        try:
            caches['compressor'].clear()
        except InvalidCacheBackendError:
            pass

    def handle(self, verbosity, *args, **options):
        self .set_options(**options)
        self.createdb_if_not_exists()
        self.clear_compressor_cache()
        call_command('migrate')
        try:
            fixture = '/web/bombay/myfixtures/bombay.json'
            call_command('loaddata', fixture)
        except Exception:
            fixture = './myfixtures/from_docker/bombay.json'
            call_command('loaddata', fixture)

        call_command('fix_filer_bug_965')
