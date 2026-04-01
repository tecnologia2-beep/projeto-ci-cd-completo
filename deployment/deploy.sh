#!/bin/bash
set -e

APP_DIR="/opt/projeto-ci-cd"
IMAGE_NAME="ghcr.io/${GITHUB_REPOSITORY_OWNER,,}/projeto-ci-cd:latest"

echo "Criando diretório da aplicação..."
mkdir -p "$APP_DIR"
cd "$APP_DIR"

echo "Criando docker-compose de produção..."
cat > docker-compose.prod.yml <<COMPOSE
services:
  mysql:
    image: mysql:8
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-p${MYSQL_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 10

  app:
    image: ${IMAGE_NAME}
    restart: always
    depends_on:
      mysql:
        condition: service_healthy
    environment:
      DB_HOST: mysql
      DB_PORT: 3306
      DB_USER: root
      DB_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      DB_NAME: ${MYSQL_DATABASE}
      PORT: 5000
    ports:
      - "5000:5000"

volumes:
  mysql_data:
COMPOSE

echo "Criando banco de dados..."
cat > init.sql <<SQL
CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};
USE ${MYSQL_DATABASE};

CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(8) UNIQUE NOT NULL,
    sec INT NOT NULL,
    Grupo CHAR(1) NOT NULL,
    Tipo_Alimento CHAR(1) NOT NULL,
    Pais CHAR(2) NOT NULL
);

INSERT IGNORE INTO produtos (codigo, sec, Grupo, Tipo_Alimento, Pais) VALUES
('BRC0001A',1,'C','A','BR'),
('BRC0002A',2,'C','A','BR'),
('BRC0003C',3,'C','C','BR');
SQL

echo "Logando no GHCR..."
echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin

echo "Baixando imagem..."
docker compose -f docker-compose.prod.yml pull

echo "Subindo containers..."
docker compose -f docker-compose.prod.yml up -d

echo "Limpando imagens antigas..."
docker image prune -f

echo "Deploy finalizado com sucesso!"
