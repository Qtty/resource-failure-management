#!/bin/bash


# Install Backend Dependencies

echo "[~] Installing Backend Dependencies"

apt update
apt install python3 python3-pip
pip3 install virtualenv
virtualenv -p /usr/bin/python3 venv
./venv/bin/pip install wheel
./venv/bin/pip install -r backend/requirements.txt

echo "[+] Backend Dependencies installed"

# Install Frontend Dependencies

echo "[~] Installing Frontend Dependencies"

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 16
nvm use 16
npm install vue
npm install -g @vue/cli

echo "[+] Frontend Dependencies installed"

# Install Docker

echo "[~] Installing Docker Dependencies"

apt install ca-certificates curl gnupg lsb-release
curl -fsSL "https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg" | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture)  signed-by=/usr/share/keyrings/docker-archive-keyring.gpg]   https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install docker-ce docker-ce-cli containerd.io
usermod -aG docker ${USER}

echo "[+] Docker installed"

# Install MongoDB

echo "[~] Installing MongoDB"

docker pull mongo
docker run --name db -d mongo

echo "[+] MongoDB Up and Running"

# Run the Frontend and the Backend

apt install tmux

echo "[~] Launching Backend"

tmux new-session -s "backend" -c ./backend -d
tmux send-keys -t "backend" "../backend.sh" Enter

echo "[~] Launching Frontend"

tmux new-session -s "frontend" -c ./frontend -d
tmux send-keys -t "frontend" "../frontend.sh" Enter 

echo "[+] Done."