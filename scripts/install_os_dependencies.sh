#!/usr/bin/env bash
apt install -y python-psycopg2 postgresql libncurses5-dev libffi libffi-devel libxml2-devel libxslt-devel libxslt1-dev
apt install -y postgresql-libs postgresql-devel python-lxml python-devel gcc patch python-setuptools
apt install -y gcc-c++ flex epel-release nginx supervisor
service nginx stop