#!/bin/bash
#python manage.py runserver 0.0.0.0:8000
#export ENVIRONMENT=development
#redis-server &
celery -A django_project worker --loglevel=info &
celery -A django_project beat --loglevel=info &
gunicorn --reload --log-level debug --bind 127.0.0.1:8000 django_project.wsgi