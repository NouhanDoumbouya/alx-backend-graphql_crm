import datetime
import requests

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes
    and optionally checks the GraphQL hello endpoint.
    """
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Heartbeat message
    message = f"{timestamp} CRM is alive\n"

    # Optional: Verify GraphQL hello field responsiveness
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            message = f"{timestamp} CRM is alive (GraphQL OK)\n"
        else:
            message = f"{timestamp} CRM is alive (GraphQL Unresponsive)\n"
    except Exception as e:
        message = f"{timestamp} CRM is alive (GraphQL Error: {e})\n"

    # Append message to log file
    with open(log_file, "a") as f:
        f.write(message)
