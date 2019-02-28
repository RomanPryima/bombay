# cd bombay_shop
# docker build -f bombay/docker-files/Dockerfile .
FROM python:3.6
LABEL Description="Run bombay-SHOP"
RUN mkdir /web
WORKDIR /web
ARG DJANGO_WORKDIR=/web/workdir
ARG DJANGO_STATIC_ROOT=/web/static
ARG DJANGO_MEDIA_ROOT=/web/media

# install packages outside of PyPI
RUN apt-get upgrade -y
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs optipng jpegoptim

# copy project relevant files into container
ADD setup.py /web/setup.py
ADD README.md /web/README.md
ADD shop /web/shop
ADD contact_us /web/contact_us
ADD email_auth /web/email_auth
ADD bombay/myshop /web/myshop
ADD requirements /web/requirements
COPY bombay/wsgi.py /web/wsgi.py
COPY bombay/manage.py /web/manage.py
COPY bombay/worker.py /web/worker.py
COPY bombay/package.json /web/package.json
COPY bombay/package-lock.json /web/package-lock.json
COPY bombay/docker-files/uwsgi.ini /web/uwsgi.ini
COPY bombay/requirements.txt /web/requirements/myshop.txt

# install project specific requirements
RUN pip install --upgrade pip
RUN pip install psycopg2-binary uWSGI 'Django<2.0' 'django-select2<6.1' 'django-angular<2.1'
RUN pip install .
RUN pip install -r /web/requirements/myshop.txt
RUN pip install --no-deps -e .
RUN npm install
RUN useradd -M -d /web -s /bin/bash django

# handle static files
ENV DJANGO_STATIC_ROOT=$DJANGO_STATIC_ROOT
ENV DJANGO_MEDIA_ROOT=$DJANGO_MEDIA_ROOT
ENV DJANGO_WORKDIR=$DJANGO_WORKDIR
RUN mkdir -p $DJANGO_STATIC_ROOT
COPY ./bombay/media  $DJANGO_MEDIA_ROOT
#COPY ./bombay/static $DJANGO_STATIC_ROOT
COPY ./bombay/myfixtures/bombay.json /web/fixtures/bombay.json
RUN mkdir -p $DJANGO_STATIC_ROOT/CACHE
#RUN python manage.py compilescss
RUN python manage.py collectstatic --noinput --ignore='*.scss'
RUN chmod -R 777 $DJANGO_STATIC_ROOT
RUN chmod -R 777 $DJANGO_MEDIA_ROOT

# handle media files in external volume
RUN mkdir -p $DJANGO_WORKDIR
RUN chown -R django.django $DJANGO_WORKDIR

# handle bombay-SHOP docs
#RUN git clone -b releases/0.13.x https://github.com/awesto/django-shop.git
#RUN cd django-shop/docs && make fragments

# keep media files in external volume
VOLUME $DJANGO_WORKDIR
