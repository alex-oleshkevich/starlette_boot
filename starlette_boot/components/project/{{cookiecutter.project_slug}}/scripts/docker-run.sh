#!/bin/bash

set -e

export DEFAULT_APP_PACKAGE=$(ls -1 */main* | grep main.py | sed -e "s/\/main.py//" | head -n 1)
export APPLICATION=${ASGI_APPLICATION:="$DEFAULT_APP_PACKAGE.main:app"}
export BIND_PORT=${GUNICORN_PORT:=8000}
export WEB_CONCURRENCY=${GUNICORN_WEB_CONCURRENCY:=1}
export LOG_LEVEL=${GUNICORN_LOG_LEVEL:='info'}
export FORWARDED_ALLOW_IPS=${GUNICORN_FORWARDED_ALLOW_IPS:='*'}
export WORKERS=${GUNICORN_WORKERS:=2}

date
alembic upgrade head

gunicorn \
 --bind 0.0.0.0:$BIND_PORT \
 --name $DEFAULT_APP_PACKAGE \
 --worker-class=uvicorn.workers.UvicornWorker \
 --workers=$WORKERS \
 --log-level=$LOG_LEVEL \
 --capture-output \
 --timeout=30 \
 --access-logfile - \
 --access-logformat '%(h)s %(l)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" - %(T)ss' \
 --error-logfile - \
 $APPLICATION
