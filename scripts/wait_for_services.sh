#!/bin/sh

# Função para verificar a disponibilidade de um serviço
wait_for_service() {
  SERVICE_NAME=$1
  HOST=$2
  PORT=$3

  echo "Aguardando o serviço $SERVICE_NAME ($HOST:$PORT) iniciar..."
  while ! nc -z $HOST $PORT; do
    sleep 1
  done
  echo "$SERVICE_NAME está pronto!"
}

# Verificar RabbitMQ
wait_for_service "RabbitMQ" "rabbitmq" 5672

# Verificar Redis
wait_for_service "Redis" "redis" 6379

echo "Todos os serviços estão prontos. Iniciando o Celery..."
exec "$@"