import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables
load_dotenv(dotenv_path='../.env') 
slack_token = os.getenv("SLACK_BOT_TOKEN")

# Check token
if not slack_token:
    print("❌ Error: SLACK_BOT_TOKEN not found in .env file.")
    exit()

# Setup Client
client = WebClient(token=slack_token)

def send_test_message():
    print("Connecting to Slack...")
    try:
        response = client.chat_postMessage(
            channel="#risk-alerts",
            text="🚨 *System Check:* SkillNova Agent is online!"
        )
        print("✅ SUCCESS! Message sent to #risk-alerts.")
    except SlackApiError as e:
        print(f"❌ Error: {e.response['error']}")

if __name__ == "__main__":
    send_test_message()