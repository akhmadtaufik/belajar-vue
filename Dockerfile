FROM python:3.8.0-slim

COPY requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /src
COPY . /src/

COPY 