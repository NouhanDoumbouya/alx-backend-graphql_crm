INSTALLED_APPS = [
    # ...
    'django_crontab',
    'crm',
]

# Add the CRONJOBS configuration
CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]
