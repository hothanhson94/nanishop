#!/bin/bash
# install dependencies
pip install -r requirements.txt

# run migrations
python manage.py migrate

# collect static files
python manage.py collectstatic --noinput
