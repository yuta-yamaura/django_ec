FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD gunicorn django2ec.wsgi --log-file -,python3 manage.py runserver 0.0.0.0:$PORT