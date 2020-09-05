#!/bin/bash

# Log Location on Server.
LOG_LOCATION=/tmp/zlogs.log

# redirect stdout/stderr to a file
# exec &> /tmp/cron_logfile.txt
exec >> /tmp/cron_logfile.txt
exec 2>&1

# exec > >(tee -i $LOG_LOCATION/MylogFile.log)
# exec 2>&1

# echo "Log Location should be: [ $LOG_LOCATION ]"



now=$(date)
echo "Current date: $now" >> /tmp/cron_test.log
print "Current date and time in Linux: %s\n" "$now" >> /tmp/cron_test.log

export DJANGO_SETTINGS_MODULE="opynfact_web_project.settings.production"
echo "Export date: $now" >> /tmp/cron_test.log

cd /home/miket2/opynfacts
source venv/bin/activate
echo "Activate date: $now" >> /tmp/cron_test.log

python product.cron.py
echo "Python date: $now" >> /tmp/cron_test.log
