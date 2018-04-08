FROM python:3.5

MAINTAINER Andre Naleavaiko <andre@gorillascode.com>

RUN mkdir -p /optilab-bi-api/logs

WORKDIR /optilab-bi-api

RUN pip install -r requirements.txt

EXPOSE 5000