#FROM python:3.11-slim-bookworm
#
## Update the package list and install required packages
#RUN apt-get update && \
#    apt-get install -y git && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
#
## Copy the application source code to the container and set the working directory
#COPY ./requirements.txt /app/requirements.txt
#COPY ./src /app/src
#
## Copy alembic files
#COPY alembic.ini alembic-upgrade.bash /app/
#
#WORKDIR /app
#
## Install Python dependencies
#RUN pip3 install --no-cache-dir --upgrade pip && \
#    pip3 install --no-cache-dir -r requirements.txt
#
## Set the user to non-root
#USER 1000


FROM python:3.11-alpine

# Set up environment variables for non-interactive installation
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
# Copy the application source code to the container
COPY ./requirements.txt /app/requirements.txt
COPY ./src /app/src
COPY alembic.ini alembic-upgrade.bash /app/


# Install system dependencies, Python dependencies, and clean up
RUN apk update && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
    && apk add --no-cache \
        git \
        ffmpeg \
        sqlite \
    && pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps && \
    rm -rf ~/.cache/pip && \
    rm -rf /var/cache/apk/*

# Set the user to non-root
USER 1000
