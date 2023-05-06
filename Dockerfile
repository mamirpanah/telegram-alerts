FROM python:3.11-slim-buster
COPY . /python-flask
WORKDIR /python-flask
RUN pip3 install -r requirements.txt && chmod -R 751 /python-flask
