FROM docker.repo.<domain-name>/library/python:3.7-slim

LABEL maintainer="Williams Gene <gene.williams@<domain-name>>"
LABEL projectId="AUTOSVC"

ENV PYTHONUNBUFFERED True
 
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN echo '[global]' > /etc/pip.conf && \
    echo 'global.index = https://repo.<domain-name>/artifactory/api/pypi/pypi/' >> /etc/pip.conf && \
    echo 'global.index-url = https://repo.<domain-name>/artifactory/api/pypi/pypi/simple' >> /etc/pip.conf && \
    pip3 install -U -r ./requirements

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
