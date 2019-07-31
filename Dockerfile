FROM python:3 as build-env

RUN mkdir -p /app
WORKDIR /app

COPY src src
COPY ./requirements.txt .
COPY ./config.json .

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./src/main.py", "--config config.json"]
