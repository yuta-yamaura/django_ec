python manage.py collectstatic --noinput
web: gunicorn config.wsgi --log-file -
release: python manage.py migrate