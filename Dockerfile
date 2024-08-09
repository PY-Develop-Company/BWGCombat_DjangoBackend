FROM python:3.11-alpine
LABEL maintainer="https://github.com/PY-Develop-Company"

ENV PYTHONUNBUFFERED 1
ENV PATH="/py/bin:$PATH"

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip
RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev

WORKDIR /app
COPY . .
EXPOSE 8000

COPY ./requirements.txt /tmp/requirements.txt
RUN python /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp &&  \
    apk del .tmp-build-deps