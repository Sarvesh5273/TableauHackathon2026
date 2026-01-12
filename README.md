# Revenue Sentinel - Tableau Hackathon 2026

## 🚀 How to Run Locally for Testing
This project uses a local Python Flask server to simulate the Salesforce Data Cloud webhook integration, working alongside the **Customer Health Command Center** dashboard in Tableau.

### Prerequisites
* Python 3.9+
* Tableau Desktop (to view the visualization)

### Installation
1. Clone this repository.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Create a `.env` file in the `scripts` folder and add your Slack Webhook URL:
   `SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/KEY`

### Running the Agent
1. **Navigate to the scripts directory:**
   `cd scripts`
   *(Crucial Step: The code requires running from this folder to locate data files)*
2. **Start the Server:**
   `python server.py`
   *(This handles the Slack interactivity and Salesforce Mock API)*
3. **Run the AI Agent (in a new terminal window):**
   `python agent.py`
   *(This analyzes the CSV telemetry and triggers the alert)*

### 🏗️ System Architecture
* **Visualization:** Tableau Dashboard ("Customer Health Command Center")
* **Backend:** Python (Flask)
* **Integration:** Slack API & Mocked Salesforce Data Cloud
* **Data Source:** Local CSV Simulation (`Usage_Logs.csv`) mimicking live telemetry.

```mermaid
graph TD
    subgraph "Data Layer"
        A[("Salesforce Data Cloud\n(Simulated CSV)")]
    end

    subgraph "The Revenue Sentinel"
        B(Python Detection Agent) -->|1. Monitors Patterns| A
        B -->|2. Detects Churn Risk| C{Risk > 30%?}
    end

    subgraph "Human-in-the-Loop"
        D[Tableau Dashboard] -->|Verifies Data| A
        C -->|Yes: Trigger Alert| E[Slack Alert Channel]
        E -->|3. Manager Clicks Approve| F(Flask Webhook Server)
    end

    subgraph "Action Layer"
        F -->|4. Trigger Retention API| G[("Salesforce CRM\n(Mock API)")]
        F -->|5. Confirmation Page| H[Success UI]
    end

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#61aec9,stroke:#333,stroke-width:2px
    style E fill:#4A154B,stroke:#333,stroke-width:2px,color:#fff