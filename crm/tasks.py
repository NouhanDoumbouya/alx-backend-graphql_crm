from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    """
    Generates a weekly CRM report by querying the GraphQL API.
    Logs total customers, orders, and revenue.
    """
    log_file = "/tmp/crm_report_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # GraphQL query to get total customers, orders, and revenue
    query = """
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json().get("data", {})
            total_customers = data.get("totalCustomers", 0)
            total_orders = data.get("totalOrders", 0)
            total_revenue = data.get("totalRevenue", 0)

            log_entry = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue"
        else:
            log_entry = f"{timestamp} - GraphQL error: {response.status_code}"

    except Exception as e:
        log_entry = f"{timestamp} - Exception: {e}"

    with open(log_file, "a") as f:
        f.write(log_entry + "\n")
