FROM python:3.6

COPY requirements.txt /tmp/
RUN python3 -m pip install -r /tmp/requirements.txt

RUN mkdir /app
WORKDIR /app

CMD ["python3", "./main.py"]
