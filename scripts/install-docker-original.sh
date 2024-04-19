#!/bin/bash
set -x
sudo apt-get update
sudo apt-get install -y gnome-terminal

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Download Docker DEB package
## TODO: Set Docker Desktop version as a variable in .env
sudo curl -o docker-desktop.deb https://desktop.docker.com/linux/main/amd64/145265/docker-desktop-4.29.0-amd64.deb

# Install Docker Desktop
sudo apt-get install -y --fix-broken ./docker-desktop.deb