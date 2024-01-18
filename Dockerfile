FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk update && apk add --no-cache postgresql-client build-base postgresql-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src .
