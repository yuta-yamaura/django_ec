FROM python:3.12
ENV PYTHONUNBUFFERED=1 DEBUG=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN mkdir -p static \
    && python3 manage.py collectstatic --no-input
CMD gunicorn config.wsgi --log-file -