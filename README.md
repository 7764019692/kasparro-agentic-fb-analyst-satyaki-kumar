📊 Kasparro Agentic FB Analyst – Assignment

Author: Satyaki Kumar
Role Applied: Applied AI Engineer – Kasparro.AI
Version: v1.0

🚀 Overview

This repository contains my submission for the Kasparro.AI Agentic FB Analyst Assignment.
The project implements an end-to-end agentic system that autonomously analyzes Meta Ads data, identifies performance drops, validates hypotheses, and recommends high-impact creatives.

The pipeline is LLM-first, fully modular, and designed using multiple cooperating agents, fulfilling all specifications mentioned in the assignment.

🎯 Key Capabilities

This system can:

📥 Load and preprocess Meta Ads dataset

📊 Generate KPI summaries (CTR, CPM, CPC, ROAS)

📉 Detect performance issues (ROAS decline, CTR drop, CPC rise)

🧪 Validate hypotheses with secondary metrics & confidence scoring

🎨 Analyze creative performance & generate improved ad copies

🤖 Use multiple agents that collaborate in sequence

🧾 Export structured outputs and execution logs

🤖 Agent Architecture

The system is built around five autonomous agents, orchestrated sequentially:

1️⃣ Data Agent

Loads dataset

Validates structure

Computes KPIs

Returns structured analysis

2️⃣ Insight Agent

Identifies:

ROAS drop

CTR decrease

CPC/CPM inflation

Creative fatigue

Produces structured findings

3️⃣ Hypothesis Agent

Validates each insight with supporting metrics

Generates confidence values

Classifies hypotheses: “validated” or “rejected”

4️⃣ Creative Agent

Analyzes past ad texts

Generates improved:

Hooks

Ad angles

CTAs

Produces final creative recommendations

5️⃣ Controller Agent

Orchestrates all agents

Handles message passing

Maintains logs

Writes final output files

📁 Project Structure (As Required)
.
├── agents/
│   ├── data_agent.py
│   ├── insight_agent.py
│   ├── hypothesis_agent.py
│   ├── creative_agent.py
│   └── controller_agent.py
│
├── data/
│   └── meta_ads_data.csv
│
├── outputs/
│   ├── insights.json
│   ├── hypotheses.json
│   ├── recommendations.json
│   └── execution_log.txt
│
├── utils/
│   ├── loader.py
│   ├── helpers.py
│   └── evaluator.py
│
├── main.py
├── requirements.txt
└── README.md


Everything follows Kasparro’s required naming + folder standards.

⚙️ Installation & Quick Start
1️⃣ Clone the Repository
git clone https://github.com/your-username/kasparro-fb-analyst.git
cd kasparro-fb-analyst

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Complete Pipeline
python main.py

5️⃣ View All Outputs

All generated files appear in:

outputs/
├── insights.json
├── hypotheses.json
├── recommendations.json
└── execution_log.txt


These include detected patterns, validated hypotheses, creative suggestions, and all execution traces.

📌 Sample Insight Output
{
  "metric": "ROAS",
  "finding": "ROAS decreased by 32% in the last 7 days",
  "root_cause": "CTR declined while CPC increased",
  "confidence": 0.91
}

📌 Sample Creative Recommendation
{
  "new_hook": "Stop scrolling — your perfect product is here!",
  "cta": "Claim your limited-time offer now!",
  "tone": "Energetic and benefit-driven"
}
