#!/usr/bin/env bash

mkdir -p /etc/nginx/sites-enabled
mkdir -p /etc/nginx/sites-available

sudo mkdir -p /etc/nginx/log/

sudo cp /home/ubuntu/www/project/nginx/default.conf /etc/nginx/nginx.conf

sudo unlink /etc/nginx/sites-enabled/*

sudo cp /home/ubuntu/www/project/nginx/prod.conf /etc/nginx/sites-available/telepsycrx.conf

sudo ln -s /etc/nginx/sites-available/telepsycrx.conf /etc/nginx/sites-enabled/telepsycrx.conf

sudo service nginx stop
sudo service nginx start
