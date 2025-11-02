#!/bin/bash
# ============================================================
# Script Name: delete_inactive_customers.sh
# Purpose: Delete customers who have had no orders for a year
# Run with: bash delete_inactive_customers.sh
# Can be added to cron for automation
# ============================================================

# Activate virtual environment if you use one (optional)
# source venv/bin/activate

# Navigate to project root (where manage.py lives)
cd "$(dirname "$0")"

# Run Django shell command
python manage.py shell <<EOF
import datetime
from django.utils import timezone
from crm.models import Customer  # ✅ Change 'crm' to your app name
from django.db.models import Q

# Calculate the cutoff date (1 year ago)
cutoff_date = timezone.now() - datetime.timedelta(days=365)

# Find customers with no orders in the last year
inactive_customers = Customer.objects.filter(
    Q(order__isnull=True) | Q(order__date__lt=cutoff_date)
).distinct()

count = inactive_customers.count()

if count > 0:
    print(f"Deleting {count} inactive customers...")
    inactive_customers.delete()
    print("✅ Successfully deleted inactive customers.")
else:
    print("ℹ️ No inactive customers found.")
EOF
