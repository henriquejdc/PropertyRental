#!/bin/sh

echo "Executando testes..."

python manage.py test --failfast manager authentication

if [ $? -ne 0 ]; then
  echo "Testes falharam. Abortando."
  exit 1
fi

coverage run --source=authentication,manager manage.py test

coverage report
coverage html

echo "Testes completos com sucesso."
exit 0
