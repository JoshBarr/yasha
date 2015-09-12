#!/bin/bash
cd /home/django/yasha
# Flush cache, deactivate venv and restart services
redis-cli FLUSHALL
service uwsgi restart
service nginx restart