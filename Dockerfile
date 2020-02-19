FROM python:3.7-alpine

WORKDIR /code

RUN apk add g++ make openssl-dev libffi-dev

COPY ./requirements.txt /code

RUN pip install -r requirements.txt

EXPOSE 8000