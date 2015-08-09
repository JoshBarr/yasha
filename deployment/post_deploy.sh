#!/bin/bash
cd ~/webapps/yasha/
# Flush cache, deactivate venv and restart services
redis-cli FLUSHALL
service uwsgi restart
# Among these two, choose your own command wisely
# apache2ctl graceful
apache2/bin/restart
# service nginx restart