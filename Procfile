web: gunicorn django_project.wsgi --log-file -
worker: celery -A django_project worker --loglevel=info
beat: celery -A django_project beat --loglevel=info
