#!/bin/bash

# Install Docker

echo "[~] Installing Docker Dependencies"

apt install ca-certificates curl gnupg lsb-release
curl -fsSL "https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg" | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture)  signed-by=/usr/share/keyrings/docker-archive-keyring.gpg]   https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install docker-ce docker-ce-cli containerd.io
usermod -aG docker ${USER}

echo "[+] Docker installed"

# Install Docker Compose

echo "[~] Installing Docker Compose"

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "[+] Docker Compose installed"

# Export DB Credentials

export DB_USERNAME=`jq -r '.db.username' backend/config.json`
export DB_PASSWORD=`jq -r '.db.password' backend/config.json`
export NGINX_PORT=`jq -r '.nginx_port' backend/config.json`

# Launching the app

echo "Application running on the port $NGINX_PORT"
sleep 5

docker-compose up --build --remove-orphans