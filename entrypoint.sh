#!/bin/bash

python manage.py migrate --noinput
python manage.py createsuperuser --username admin --email corey.bodendein@gmail.com --noinput

exec "$@"
