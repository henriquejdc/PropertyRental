#!/bin/sh

echo "Iniciando o servidor Django..."
python manage.py runserver 0.0.0.0:8000
#NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python manage.py runserver
