#!/bin/sh

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput
