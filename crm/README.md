# CRM Celery & Report Automation Setup Guide

This document explains how to configure and run **Celery**, **Celery Beat**, and **Redis** to automate CRM report generation in the **alx-backend-graphql_crm** project.

---

## 🧩 Prerequisites

Ensure you have the following installed:

* Python 3.8+
* Django
* Redis Server (`redis-server`)
* Celery
* django-celery-beat

---

## ⚙️ Installation & Setup

### 1. Install Redis and Dependencies

```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# Verify Redis is running
redis-cli ping
# Should respond: PONG
```

### 2. Install Python Requirements

Ensure `requirements.txt` includes:

```
Django
celery
django-celery-beat
redis
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Django Setup

### 3. Apply Database Migrations

```bash
python manage.py migrate
```

### 4. Verify Installed Apps in `crm/settings.py`

Ensure the following apps are included:

```python
INSTALLED_APPS = [
    ...,
    'django_celery_beat',
]
```

---

## 🚀 Celery Configuration

### 5. Celery Initialization in `crm/celery.py`

Your `crm/celery.py` should look like:

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### 6. Load Celery in `crm/__init__.py`

```python
from .celery import app as celery_app
__all__ = ('celery_app',)
```

---

## 📊 Weekly Report Task Configuration

### 7. Define Task in `crm/tasks.py`

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

    print("CRM Report generated successfully!")
```

---

## ⏰ Celery Beat Schedule

### 8. Configure Beat Schedule in `crm/settings.py`

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

---

## 🧠 Running Celery

### 9. Start the Celery Worker

```bash
celery -A crm worker -l info
```

### 10. Start Celery Beat Scheduler

```bash
celery -A crm beat -l info
```

---

## ✅ Verification

### 11. Check Logs

After the first scheduled run, verify the log file:

```bash
cat /tmp/crm_report_log.txt
```

Expected format:

```
2025-11-02 06:00:00 - Report: 50 customers, 120 orders, 7800 revenue
```

---

## 🧾 Summary

| Step | Description                  |
| ---- | ---------------------------- |
| 1    | Install Redis                |
| 2    | Install dependencies         |
| 3    | Run migrations               |
| 4    | Verify `INSTALLED_APPS`      |
| 5    | Create `crm/celery.py`       |
| 6    | Load Celery in `__init__.py` |
| 7    | Define Celery Task           |
| 8    | Add Beat Schedule            |
| 9    | Run Celery Worker            |
| 10   | Run Celery Beat              |
| 11   | Verify Log Output            |

---

🎯 **Done!**
Your CRM now automatically generates weekly reports via Celery and Celery Beat.
