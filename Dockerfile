FROM python:3 as build-env

RUN mkdir -p /app
WORKDIR /app

COPY src src
COPY ./requirements.txt .

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./src/main.py"]
