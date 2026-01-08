import pandas as pd
import requests
import time

# --- CONFIGURATION ---
LOGS_FILE = '../data/Usage_Logs.csv'
SERVER_URL = 'http://127.0.0.1:5000/webhook/churn-alert'
TARGET_ACCOUNT = 'Acme Corp'
TARGET_ID = "ACC-1000"

def calculate_retention_offer(drop_rate):
    """
    🤖 THE AI LOGIC:
    Dynamically calculates the discount based on the severity of the drop.
    """
    if drop_rate > 50:
        return "30% Discount (Tier 1 Save)", "CRITICAL"
    elif drop_rate > 30:
        return "15% Discount (Standard Save)", "HIGH"
    else:
        return "Check-in Call Only", "MEDIUM"

def analyze_churn_risk():
    print(f"🕵️ AGENT: Reading Usage Logs from {LOGS_FILE}...")
    
    # 1. Load Data
    try:
        df = pd.read_csv(LOGS_FILE)
    except FileNotFoundError:
        print("❌ Error: Usage_Logs.csv not found!")
        return

    # 2. Filter for Acme Corp
    client_logs = df[df['Account_ID'] == TARGET_ID].copy()
    
    # 3. Analyze Trend
    client_logs['Date'] = pd.to_datetime(client_logs['Date'])
    client_logs = client_logs.sort_values(by='Date')
    
    recent_activity = client_logs.tail(5)['Active_Users'].mean()
    previous_activity = client_logs.iloc[-10:-5]['Active_Users'].mean()
    
    drop_rate = ((previous_activity - recent_activity) / previous_activity) * 100
    
    # 4. 🤖 AI DECISION MAKING
    offer, risk_level = calculate_retention_offer(drop_rate)

    print(f"📊 ANALYSIS: {TARGET_ACCOUNT}")
    print(f"   - Drop Rate:  {drop_rate:.1f}%")
    print(f"   - Risk Level: {risk_level}")
    print(f"   - AI Suggestion: {offer}")

    # 5. Trigger Alert
    if drop_rate > 30:
        print("🚨 RISK DETECTED! Triggering Slack Agent...")
        
        # We send the RAW DATA to the server, letting the server format the buttons
        payload = {
            "account_name": TARGET_ACCOUNT,
            "drop_percent": f"{drop_rate:.0f}%",
            "risk_level": risk_level,
            "suggested_offer": offer
        }
        
        try:
            requests.post(SERVER_URL, json=payload)
            print("✅ SENT: Alert pushed to Slack.")
        except Exception as e:
            print(f"❌ FAILED: Is server.py running? {e}")

if __name__ == "__main__":
    print("--- 🤖 STARTING CHURN SENTINEL ---")
    analyze_churn_risk()