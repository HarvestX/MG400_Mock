FROM python:3.6

RUN pip install uwsgi flask
RUN mkdir /app
WORKDIR /app

CMD ["uwsgi", "--ini", "/app/config/uwsgi.ini"]
