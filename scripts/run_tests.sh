#!/bin/sh

echo "Executando testes..."
python manage.py test --failfast manager authentication
coverage run --source='./manager' manage.py test
coverage report
coverage html