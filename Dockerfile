FROM python:3.11.0a4-alpine3.15
MAINTAINER Joe Buckley Django Practice

ENV PYTHONUNBUFFERED 1

COPY ./requirments.txt /requirments.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirments.txt

RUN apk del .tmp-build-deps

RUN mkdir /app

RUN adduser -D dockuser
RUN chown dockuser /app
#USER dockuser

WORKDIR /app
COPY ./app /app