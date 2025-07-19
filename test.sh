#!/bin/bash
# test.sh

# Run migrations
python manage.py migrate

# Run tests
pytest
