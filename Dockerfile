FROM python:latest

RUN mkdir /usr/src/user-account-api

COPY requirements.txt /usr/src/user-account-api/requirements.txt

WORKDIR /usr/src/user-account-api/

EXPOSE 5000

#RUN apt-get update \
#    && apt-get upgrade -y \
#    && pip install virtualenv \
#    && python3 -m venv env \
#    && source env/bin/acitvate \
#    && pip install --upgrade pip \
#    && pip install --no-cache-dir -r requirements.txt \
#    && pip install pkce \
#    && pip install fusionauth-client \
#    && pip freeze > requirements.txt 



