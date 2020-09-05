now=$(date)
echo "Current date: $now" >> /tmp/cron_test.log
print "Current date and time in Linux: %s\n" "$now" >> /tmp/cron_test.log

export DJANGO_SETTINGS_MODULE="opynfact_web_project.settings.production"

cd /home/miket2/opynfacts
source venv/bin/activate

python product.cron.py