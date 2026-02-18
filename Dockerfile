FROM python:3.8

COPY requirements.txt /tmp/
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /app
WORKDIR /app

COPY ./app/src/ /app/

CMD ["python3", "./main.py"]
