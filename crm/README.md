# CRM Celery Weekly Report Setup Guide

This guide explains how to configure **Celery** and **Celery Beat** to automatically generate a **weekly CRM report** integrating with the **GraphQL schema**.

---

## 🎯 Objective

Configure a Celery task with Celery Beat to:

* Generate a **weekly CRM report** summarizing:

  * Total number of customers
  * Total number of orders
  * Total revenue (sum of `totalamount` from orders)
* Log the report to `/tmp/crm_report_log.txt` with a timestamp.

---

## 🧩 1. Set Up Celery

### Add Dependencies

In `requirements.txt`, ensure these packages are listed:

```
celery
django-celery-beat
redis
```

### Update Installed Apps

In `crm/settings.py`, add:

```python
INSTALLED_APPS = [
    ...,
    'django_celery_beat',
]
```

### Initialize Celery

Create `crm/celery.py`:

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### Load Celery in `crm/__init__.py`

```python
from .celery import app as celery_app
__all__ = ('celery_app',)
```

### Configure Redis as Broker

In `crm/settings.py`, add:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

---

## 🧠 2. Define the Celery Task

Create `crm/tasks.py`:

```python
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """)

    result = client.execute(query)
    customers = result.get('totalCustomers', 0)
    orders = result.get('totalOrders', 0)
    revenue = result.get('totalRevenue', 0)

    with open("/tmp/crm_report_log.txt", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")

    print("CRM report generated successfully!")
```

---

## ⏰ 3. Schedule with Celery Beat

In `crm/settings.py`, configure Celery Beat to run weekly on Monday at 6:00 AM:

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
```

---

## ⚙️ 4. Document Setup Steps

### Install Redis

```bash
sudo apt update
sudo apt install redis-server
```

Verify Redis is running:

```bash
redis-cli ping
# Output: PONG
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Celery Worker

```bash
celery -A crm worker -l info
```

### Start Celery Beat

```bash
celery -A crm beat -l info
```

---

## ✅ 5. Verify Logs

After the first scheduled run, check:

```bash
cat /tmp/crm_report_log.txt
```

Expected output format:

```
2025-11-02 06:00:00 - Report: 80 customers, 145 orders, 12000 revenue
```

---

## 📘 Repository

**GitHub Repository:** `alx-backend-graphql_crm`
**Files Involved:**

* `crm/celery.py`
* `crm/tasks.py`
* `crm/settings.py`
* `crm/__init__.py`
* `requirements.txt`
* `crm/README.md`

---

🎉 **Done!**
Your Celery task is now configured to automatically generate and log CRM reports weekly using Redis and Celery Beat.
