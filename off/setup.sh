#!/bin/bash

echo "Обновляем систему..."
apt update && apt install -y docker.io docker-compose git

echo "Клонируем проект (если нужно)..."
# git clone ... (если будет репозиторий)

echo "Запускаем Docker Compose..."
docker-compose up -d --build
