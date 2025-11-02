import datetime
import requests
# "from gql.transport.requests import RequestsHTTPTransport", "from gql import", "gql", "Client"
def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes
    and verifies GraphQL hello endpoint.
    """
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    message = f"{timestamp} CRM is alive"

    # Optional GraphQL hello check
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("data", {}).get("hello"):
                message += " (GraphQL OK)"
            else:
                message += " (GraphQL Response Invalid)"
        else:
            message += f" (GraphQL HTTP {response.status_code})"
    except Exception as e:
        message += f" (GraphQL Error: {e})"

    # Write heartbeat log
    with open(log_file, "a") as f:
        f.write(message + "\n")

import datetime
import requests

def update_low_stock():
    """
    Executes the GraphQL mutation to restock low-stock products
    and logs the updates to /tmp/low_stock_updates_log.txt
    """
    log_file = "/tmp/low_stock_updates_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    query = """
    mutation {
        updateLowStockProducts {
            message
            updatedProducts {
                name
                stock
            }
        }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=10
        )

        log_entry = f"{timestamp} "

        if response.status_code == 200:
            data = response.json().get("data", {}).get("updateLowStockProducts", {})
            message = data.get("message", "No message")
            products = data.get("updatedProducts", [])
            log_entry += f"{message}\n"

            for p in products:
                log_entry += f"  - {p['name']}: stock now {p['stock']}\n"
        else:
            log_entry += f"GraphQL HTTP error {response.status_code}\n"

    except Exception as e:
        log_entry = f"{timestamp} GraphQL Error: {e}\n"

    with open(log_file, "a") as f:
        f.write(log_entry + "\n")
