#!/bin/sh
# Use this to install software packages
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
sudo dpkg -i session-manager-plugin.deb
sudo apt-get update -y
sudo apt-get -y install apache2
sudo ufw allow 'Apache'
sudo systemctl enable --now apache2