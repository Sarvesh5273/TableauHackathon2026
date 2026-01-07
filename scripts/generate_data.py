import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize
fake = Faker()
random.seed(42) # Ensures we get the same "random" data every time

# Configuration
NUM_ACCOUNTS = 20
DAYS_HISTORY = 30
HERO_CLIENT = "Acme Corp" # This is our target for the demo

def generate_data():
    print(f"⚙️ Generating data for {NUM_ACCOUNTS} accounts...")

    # --- 1. Generate Accounts ---
    accounts = []
    for i in range(NUM_ACCOUNTS):
        is_hero = (i == 0)
        account = {
            "Account_ID": f"ACC-{1000+i}",
            "Account_Name": HERO_CLIENT if is_hero else fake.company(),
            "Industry": "Tech" if is_hero else random.choice(["Retail", "Finance", "Healthcare"]),
            "Tier": "Enterprise" if is_hero else random.choice(["Standard", "Pro"]),
            "ARR": 120000 if is_hero else random.randint(10000, 80000)
        }
        accounts.append(account)
    
    # --- 2. Generate Usage Logs ---
    logs = []
    start_date = datetime.now() - timedelta(days=DAYS_HISTORY)

    for acc in accounts:
        # Each client has a "baseline" of daily logins
        base_usage = random.randint(50, 200)
        
        for day in range(DAYS_HISTORY):
            current_date = start_date + timedelta(days=day)
            
            # Normal fluctuation
            daily_usage = int(base_usage * random.uniform(0.9, 1.1))
            errors = random.randint(0, 2)
            
            # THE TRAP: Make Acme Corp usage drop 50% in the last 5 days
            if acc["Account_Name"] == HERO_CLIENT and day > (DAYS_HISTORY - 5):
                daily_usage = int(base_usage * 0.5)  # CRASH
                errors = random.randint(15, 20)      # SPIKE
            
            logs.append({
                "Log_ID": fake.uuid4(),
                "Account_ID": acc["Account_ID"],
                "Date": current_date.strftime("%Y-%m-%d"),
                "Active_Users": daily_usage,
                "Errors": errors
            })

    # --- 3. Save to Data Folder ---
    pd.DataFrame(accounts).to_csv('../data/Accounts.csv', index=False)
    pd.DataFrame(logs).to_csv('../data/Usage_Logs.csv', index=False)
    print("✅ DONE: Accounts.csv and Usage_Logs.csv created in /data folder.")

if __name__ == "__main__":
    generate_data()