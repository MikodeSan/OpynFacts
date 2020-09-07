#!/bin/bash

# Log Location on Server.
# LOG_LOCATION=/tmp/zlogs.log

# redirect stdout/stderr to a file
# exec &> /tmp/cron_logfile.txt
# exec >> /tmp/cron_logfile.txt
# exec 2>&1

# exec > >(tee -i $LOG_LOCATION/MylogFile.log)
# exec 2>&1

# echo "Log Location should be: [ $LOG_LOCATION ]"


now=$(date)
echo "CRONJOB START: $now" > /tmp/djg_opnfct_cron_sh.log
# print "Current date and time in Linux: %s\n" "$now" >> /tmp/cron_test.log

export PRODUCTION
export DJANGO_SETTINGS_MODULE="opynfact_web_project.settings.production"

# cd /home/user/opynfacts
# source venv/bin/activate

# python product.cron.py
/home/miket2/opynfact/venv/bin/python /home/miket2/opynfact/manage.py initializedatabase 0 >> /tmp/djg_opnfct_cron_sh.log
now=$(date)
echo "CRONJOB END: $now" >> /tmp/djg_opnfct_cron_sh.log
