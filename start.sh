#!/bin/bash

# echo "Running tests..."
# pytest

# Run migrations
alembic upgrade head

if [ $? -eq 0 ]; then
  echo "Tests passed! Starting the application..."
  gunicorn -c gunicorn_config.py app:app
else
  echo "Tests failed! Fix the issues and try again."
fi
