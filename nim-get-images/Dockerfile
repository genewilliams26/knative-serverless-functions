FROM docker.repo.<domain-name>/library/python:3.7-slim
 
ENV PYTHONUNBUFFERED True
 
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
 
RUN pip install -i https://repo.<domain-name>/artifactory/api/pypi/pypi/simple -r requirements
 
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
