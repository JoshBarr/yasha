#!/bin/bash

# This script needs the following 3 parameters to work properly: USERNAME, DOMAIN, SETTINGS
# Example:
# $ ./deploy.sh site site.co.nz site.settings.production
# It could be improved but it's a starting point
cd /home/yasha/yasha

USERNAME=$1
DOMAIN=$2
SETTINGS=$3

sudo yasha
# Activate virtual environment
source yashaenv/bin/activate
# cd /var/www/$USERNAME/$DOMAIN/$USERNAME

# Install requirements in case there are new dependencies or updates
if [ -f requirements/production.txt ]; then
    pip install -r requirements/production.txt
fi

# Check for migrations
output="$(python manage.py migrate --settings=${SETTINGS}  --list | grep "\[ ]" | wc -l)"

if [ $output -ge 1 ]
then
  ./manage.py migrate --settings=$SETTINGS
else
  echo "No migrations to run"
fi

# A bit of clean-up
python manage.py collectstatic --noinput --settings=$SETTINGS
python manage.py compress --settings=$SETTINGS
python manage.py update_index --settings=$SETTINGS

deactivate
