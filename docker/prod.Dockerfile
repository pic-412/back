FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /back && chmod -R 755 /back

WORKDIR /back
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .