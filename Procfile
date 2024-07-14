web: gunicorn config.wsgi --log-file -
python manage.py collectstatic --noinput
release: python manage.py migrate