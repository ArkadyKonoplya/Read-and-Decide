#!/usr/bin/env bash
cd /home/ubuntu/www/project/
# python3 manage.py makemigrations accounts, notes, personal_journal, telepsycrx_admin, telepsycrx_billing, telepsycrx_hr, telepsycrx_marketing, telePsycRxEmployees

python3 manage.py migrate accounts
python3 manage.py migrate notes
python3 manage.py migrate personal_journal
python3 manage.py migrate telepsycrx_admin
python3 manage.py migrate telepsycrx_billing
python3 manage.py migrate telepsycrx_hr
python3 manage.py migrate telepsycrx_marketing
python3 manage.py migrate telePsycRxEmployees
# python3 manage.py migrate



# source /home/ubuntu/www/project-venv/bin/activate
# DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 ./manage.py makemigrations
# DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 ./manage.py migrate auth
# DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 ./manage.py migrate