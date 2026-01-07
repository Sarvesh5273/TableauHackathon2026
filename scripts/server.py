from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 1. Setup
load_dotenv(dotenv_path='../.env')
app = Flask(__name__)
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

# 2. The Trigger Endpoint
@app.route('/webhook/churn-alert', methods=['POST'])
def trigger_alert():
    data = request.json
    print(f"📩 Received Alert for: {data.get('account_name')}")

    # Extract details from the request
    account_name = data.get('account_name', 'Unknown Client')
    drop_percent = data.get('drop_percent', '0%')

    # 3. Send to Slack
    try:
        message = (
            f"🚨 *Risk Detected via Tableau*\n"
            f"**Client:** {account_name}\n"
            f"**Usage Drop:** {drop_percent}\n"
            f"👉 *Agent Action:* Generated 20% Retention Offer."
        )
        
        client.chat_postMessage(channel="#risk-alerts", text=message)
        return jsonify({"status": "success", "message": "Alert sent to Slack"}), 200

    except SlackApiError as e:
        return jsonify({"status": "error", "error": str(e)}), 500

# 4. Start Server
if __name__ == '__main__':
    print("🌍 Server is running on port 5000...")
    app.run(port=5000, debug=True)