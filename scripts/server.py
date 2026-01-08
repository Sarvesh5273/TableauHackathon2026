import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests
import json

# Load secrets
load_dotenv()

app = Flask(__name__)

# --- CONFIGURATION ---
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

if not SLACK_WEBHOOK_URL:
    print("❌ CRITICAL ERROR: SLACK_WEBHOOK_URL not found in .env file.")
    exit(1)

# --- 1. THE WEBHOOK (Receives Data from Python) ---
@app.route('/webhook/churn-alert', methods=['POST'])
def handle_churn_alert():
    data = request.json
    
    account = data.get('account_name')
    drop = data.get('drop_percent')
    offer = data.get('suggested_offer')
    
    # Block Kit with Local URL
    slack_payload = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🚨 Churn Risk Detected"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Client:*\n{account}"},
                    {"type": "mrkdwn", "text": f"*Usage Drop:*\n{drop}"}
                ]
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"🤖 *AI Recommendation:* \nGenerated {offer}"}
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "✅ Approve Offer"},
                        "style": "primary",
                        "url": "http://127.0.0.1:5000/action-confirmed"  # Points to your new stylish page
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "❌ Reject"},
                        "style": "danger"
                    }
                ]
            }
        ]
    }

    try:
        requests.post(SLACK_WEBHOOK_URL, json=slack_payload)
        print("✅ Message delivered to Slack.")
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
    
    return jsonify({"status": "success"}), 200


# --- 2. THE STYLISH SUCCESS PAGE (HTML + CSS) ---
@app.route('/action-confirmed', methods=['GET'])
def action_confirmed():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Action Confirmed</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background: linear-gradient(135deg, #3a7bd5 0%, #3a6073 100%); /* Enterprise Blue Gradient */
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #333;
            }
            .card {
                background: white;
                padding: 50px;
                border-radius: 16px;
                box-shadow: 0 20px 50px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 450px;
                width: 90%;
                animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            .icon-circle {
                width: 80px;
                height: 80px;
                background: #e8f5e9;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 25px auto;
            }
            .icon-check {
                color: #2e7d32;
                font-size: 40px;
            }
            h1 {
                font-size: 28px;
                margin-bottom: 10px;
                color: #1a202c;
            }
            p.subtitle {
                color: #718096;
                font-size: 16px;
                line-height: 1.5;
                margin-bottom: 30px;
            }
            .details-box {
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                text-align: left;
                margin-bottom: 30px;
            }
            .detail-row {
                display: flex;
                align-items: center;
                margin-bottom: 8px;
                font-size: 14px;
                color: #4a5568;
            }
            .detail-icon { margin-right: 10px; }
            .btn {
                background: #3182ce;
                color: white;
                border: none;
                padding: 14px 40px;
                font-size: 16px;
                font-weight: 600;
                border-radius: 8px;
                cursor: pointer;
                width: 100%;
                transition: all 0.2s ease;
                box-shadow: 0 4px 14px rgba(49, 130, 206, 0.4);
            }
            .btn:hover {
                transform: translateY(-2px);
                background: #2b6cb0;
            }
            .footer {
                margin-top: 20px;
                font-size: 12px;
                color: #a0aec0;
            }
            @keyframes popIn {
                from { transform: scale(0.8); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="icon-circle">
                <div class="icon-check">✔</div>
            </div>
            <h1>Action Confirmed</h1>
            <p class="subtitle">The retention offer (15%) has been successfully dispatched to <strong>Acme Corp</strong>.</p>
            
            <div class="details-box">
                <div class="detail-row">
                    <span class="detail-icon">📄</span> 
                    <strong>Campaign ID:</strong> &nbsp; #RET-2026-X99
                </div>
                <div class="detail-row">
                    <span class="detail-icon">📡</span> 
                    <strong>Status:</strong> &nbsp; <span style="color: #2e7d32; font-weight: bold;">● Sent via Salesforce API</span>
                </div>
            </div>

            <button class="btn" onclick="window.close()">Close Window</button>
            <div class="footer">🔒 Secure Transaction • SkillNova Agent</div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 ENTERPRISE SERVER RUNNING on Port 5000...")
    app.run(port=5000)