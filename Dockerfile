FROM python:3.9.12-alpine3.15


WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

