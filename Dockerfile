FROM python:3.12-alpine AS build
RUN python3.12 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel

COPY pyproject.toml /pyproject.toml
COPY requirements.txt /requirements.txt
COPY src /src
RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev libpq-dev && \
    apk add --no-cache libxslt && \
    /venv/bin/pip install --disable-pip-version-check -e / && \
    apk del .build-deps

COPY . .
WORKDIR /src

ENTRYPOINT ["/venv/bin/python3", "main.py"]