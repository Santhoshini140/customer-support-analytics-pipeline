import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

issue_types = [
    "Payment Issue",
    "Refund Request",
    "Login Problem",
    "Account Locked",
    "Order Delay",
    "Product Defect",
    "Shipping Issue",
    "Subscription Cancellation"
]

priorities = ["Low", "Medium", "High", "Critical"]
statuses = ["Open", "In Progress", "Resolved", "Closed"]

agents = [
    "Alice",
    "Bob",
    "Charlie",
    "David",
    "Emma",
    "Sophia",
    "James",
    "Michael"
]

rows = []

for ticket_id in range(1, 1001):

    created_date = fake.date_time_between(start_date="-90d", end_date="now")

    status = random.choice(statuses)

    if status in ["Resolved", "Closed"]:
        resolved_date = created_date + timedelta(days=random.randint(1, 10))
        satisfaction = random.randint(1, 5)
    else:
        resolved_date = None
        satisfaction = None

    rows.append({
        "ticket_id": ticket_id,
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "issue_type": random.choice(issue_types),
        "priority": random.choice(priorities),
        "status": status,
        "agent_name": random.choice(agents),
        "created_date": created_date,
        "resolved_date": resolved_date,
        "satisfaction_score": satisfaction
    })

df = pd.DataFrame(rows)

df.to_csv("data/raw/customer_support_tickets.csv", index=False)

print("Dataset created successfully!")
print(df.head())