# app/Dockerfile

# pull the official docker image
FROM python:3.11.2-slim

# set work directory
WORKDIR /bb

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY .. .