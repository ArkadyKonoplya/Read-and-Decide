#!/usr/bin/env bash
chown ubuntu:ubuntu /home/ubuntu/www
cd /home/ubuntu/www
sudo apt install python3-venv 
/usr/bin/python3 -m venv venv 
source venv/bin/activate 
# venv /home/ubuntu/www/venv
# source /home/ubuntu/www/venv/bin/activate
pip3 install gunicorn
pip3 install -r /home/ubuntu/www/project/requirements.txt




# chown ubuntu:ubuntu /home/ubuntu/www/project-venv
# chown ubuntu:ubuntu /home/ubuntu/www/project-venv/*
