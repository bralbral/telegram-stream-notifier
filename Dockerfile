FROM python:3.12-alpine

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
