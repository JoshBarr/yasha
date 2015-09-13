#!/bin/bash
cd /home/yasha/yasha
# Flush cache, deactivate venv and restart services
redis-cli FLUSHALL
service gunicorn restart
service nginx restart