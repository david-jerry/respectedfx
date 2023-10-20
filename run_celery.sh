#!/bin/bash

# Check if Redis server is running
redis_status=$(ps -ef | grep -v grep | grep redis-server)

if [ -z "$redis_status" ]; then
    echo "Redis server is not running."
    exit 1
else
    echo "Redis server is running. Starting Celery script."
    # Replace 'config.celery_app' with your actual Celery application name
    celery -A config.celery_app worker --loglevel=info
fi
