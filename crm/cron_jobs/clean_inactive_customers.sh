#!/bin/bash

# File: crm/cron_jobs/clean_inactive_customers.sh
# Purpose: Delete customers with no orders in the past year and log the result.

# Activate virtual environment (optional if needed)
# source /path/to/venv/bin/activate

# Run Django shell command to delete inactive customers
deleted_count=$(python manage.py shell <<EOF
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True) | Customer.objects.exclude(order__date__gte=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

# Log output with timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
