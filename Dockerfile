FROM python:3.5

MAINTAINER Andre Naleavaiko <andre@gorillascode.com>

ADD . /optilab-bi-api

RUN mkdir -p /optilab-bi-api/logs

RUN apt-get update && apt-get install -y libfbclient2

WORKDIR /optilab-bi-api

RUN pip install --upgrade pip
RUN pip install gunicorn eventlet
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--config=gunicorn.py", "run:app"]
