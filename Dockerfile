FROM python:latest

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements/development.txt

EXPOSE 8000
EXPOSE 5432
