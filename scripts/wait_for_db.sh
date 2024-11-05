#!/bin/sh

# Aguarda o banco de dados ficar disponível
until nc -z -v -w30 postgresql 5432
do
  echo "Aguardando o banco de dados ficar disponível..."
  sleep 1
done

echo "Banco de dados está disponível. Iniciando migrações e o servidor Django."
exec "$@"