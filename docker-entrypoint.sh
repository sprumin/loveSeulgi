#!/bin/bash

echo "Update model migration"
python manage.py makemigrations --settings=LoveSeulgi.settings.production

echo "Django Databases migration"
python manage.py migrate --settings=LoveSeulgi.settings.production

echo "Start Django Server"
uwsgi --http :8000 --module LoveSeulgi.wsgi --enable-threads --processes 4
