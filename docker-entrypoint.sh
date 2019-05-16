#!/bin/bash

echo "Update model migration"
python manage.py makemigrations

echo "Django Databases migration"
python manage.py migrate

echo "Start Django Server"
python manage.py runserver 0:8000 --settings=LoveSeulgi.settings.development 
