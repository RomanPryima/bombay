#!/bin/sh
mkdir -p ../bombay/myfixtures/from_docker
./manage.py dumpdata --indent=2 --natural-foreign email_auth cms cmsplugin_cascade djangocms_text_ckeditor filer post_office shop myshop --exclude cmsplugin_cascade.segmentation --exclude filer.clipboard --exclude filer.clipboarditem --exclude myshop.cart --exclude myshop.cartitem > ../bombay/myfixtures/bombay.json
