#!/usr/bin/env bash
set -eu
cmd="$@"

/wait-for-it.sh -t 10 $DATABASE_HOST:$DATABASE_PORT

python manage.py makemigrations
python manage.py migrate
python manage.py createinitialsuperuser --noinput


if [ -z "$cmd" ]
then
	python manage.py runserver 0.0.0.0:8000
else
	exec $cmd
fi