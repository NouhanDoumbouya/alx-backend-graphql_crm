import datetime
import requests

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
