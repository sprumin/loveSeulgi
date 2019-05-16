#!/bin/bash

echo "Update model migration"
python manage.py makemigrations --settings=LoveSeulgi.settings.development

echo "Django Databases migration"
python manage.py migrate --settings=LoveSeulgi.settings.development

echo "Start Django Server"
python manage.py runserver 0:8000 --settings=LoveSeulgi.settings.development 
