#!/bin/sh

echo "Iniciando o servidor Django..."
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python manage.py runserver
