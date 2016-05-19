#! /bin/bash

cd /project/projectdirs/cosmo/webapp/viewer
source ./venv/bin/activate
export PYTHONPATH=${PYTHONPATH}:$(pwd)/venv
#export PYTHONPATH=${PYTHONPATH}:$(pwd)/venv/lib/python2.7:$(pwd)/venv
#export PATH=$(pwd)/venv/bin:${PATH}

uwsgi -s :3031 --wsgi-file wsgi.py --touch-reload wsgi.py --processes 8 --reload-on-rss 768 --logto /tmp/uwsgi.log -d /tmp/uwsgi2.log

