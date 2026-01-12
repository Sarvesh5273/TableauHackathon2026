# Revenue Sentinel - Tableau Hackathon 2026

## 🚀 How to Run Locally for Testing
This project uses a local Python Flask server to simulate the Salesforce Data Cloud webhook integration.

### Prerequisites
* Python 3.9+
* Tableau Desktop (to view the dashboard file)

### Installation
1. Clone this repository.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Create a `.env` file and add your Slack Webhook URL:
   `SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/KEY`

### Running the Agent
1. **Start the Server:**
   `python server.py`
   *(This handles the Slack interactivity and Salesforce Mock API)*
2. **Run the AI Agent:**
   `python agent.py`
   *(This analyzes the CSV telemetry and triggers the alert)*

### Architecture
* **Visualization:** Tableau Dashboard (included as `Revenue_Sentinel.twbx`)
* **Backend:** Python (Flask)
* **Integration:** Slack API & Mocked Salesforce Data Cloud