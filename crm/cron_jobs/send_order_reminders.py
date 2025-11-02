#!/usr/bin/env python3
"""
====================================================
Script Name: send_order_reminders.py
Purpose: Query GraphQL endpoint for recent orders (7 days)
         and log reminders for pending orders
Schedule: Daily (8:00 AM)
====================================================
"""

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def main():
    # Define date range for last 7 days
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    # Setup GraphQL client
    transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT, verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query to fetch recent orders
    query = gql(
        """
        query GetRecentOrders($startDate: Date!) {
            orders(filter: { orderDate_Gte: $startDate }) {
                id
                orderDate
                customer {
                    email
                }
            }
        }
        """
    )

    # Execute query
    result = client.execute(query, variable_values={"startDate": str(week_ago)})

    # Extract orders
    orders = result.get("orders", [])

    # Write log
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n[{timestamp}] Order Reminder Run\n")
        if not orders:
            f.write("No recent pending orders.\n")
        else:
            for order in orders:
                f.write(f"Order ID: {order['id']} | Customer: {order['customer']['email']}\n")

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
