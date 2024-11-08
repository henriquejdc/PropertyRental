#!/bin/sh
# Script to wait for the Django service to be ready

HOST="django"  # Nome do serviço do Django no Docker Compose
PORT=8000      # Porta em que o Django está exposto

echo "Aguardando o serviço Django iniciar em $HOST:$PORT..."

# Loop até que a conexão com Django esteja disponível
while ! nc -z $HOST $PORT; do
  echo "Django ainda não está pronto. Tentando novamente em 80 segundos..."
  sleep 80
done

echo "Django está pronto! Continuando..."
