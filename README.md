🔥 Operon — AI-Powered Business Automation Platform

Operon is an AI-driven system that captures inbound leads, analyzes intent, prioritizes opportunities, and automatically generates intelligent follow-ups.

Built to simulate how modern AI-first businesses handle sales pipelines.

🚀 Core Features

🔹 Multi-Channel Lead Ingestion
Website form submissions
WhatsApp webhook integration

🔹 AI Lead Analysis (LLM #1)
Each lead is analyzed to generate:
Intent classification
Lead score (0–100)
Priority category (High / Medium / Low)
Confidence score
Reasoning

🔹 Intelligent Scoring System
Factor Weight
Clear Intent +30
Urgency +40
Budget +20
Specific Details +10

🔹 Workflow Automation
Automated decision engine:
Score ≥ 80 → Immediate Action
Score 40–79 → Follow-up
Score < 40 → Nurture

🔹 AI Reply Generation (LLM #2)
Generates:
Context-aware
Professional
Personalized responses

🔹 Admin Dashboard
Lead overview
AI decision breakdown
Action tracking
AI-generated replies

🔹 Structured Logging

System logs:
AI decisions
Workflow actions
Errors
API events

🧠 System Architecture
Client (Form / WhatsApp)
↓
FastAPI Backend
↓
AI Engine (LLM #1)
↓
Workflow Engine
↓
Reply Engine (LLM #2)
↓
Database (SQLite)
↓
Next.js Dashboard

⚙️ Tech Stack
Backend
FastAPI
SQLAlchemy
SQLite

Frontend
Next.js
Tailwind CSS

AI
Groq API (LLMs)

🔌 WhatsApp Integration (MVP)
Operon supports inbound WhatsApp messages via webhook.

Endpoint
POST /webhook/whatsapp

Sample Payload
{
"entry": [{
"changes": [{
"value": {
"messages": [{
"from": "919999999999",
"text": {
"body": "Need automation ASAP, budget 5k"
}
}]
}
}]
}]
}

🧪 Running Locally

1. Clone repo
   git clone <repo-url>
   cd Operon2
2. Backend setup
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
3. Frontend setup
   cd frontend/nextjs-dashboard
   npm install
   npm run dev
4. Open dashboard
   http://localhost:3000

📂 Project Structure
backend/
app/
api/
services/
database/
schemas/

frontend/
nextjs-dashboard/

⚠️ MVP Limitations
No real WhatsApp API (webhook simulated)
No authentication
No conversation threads
No deployment yet

🔮 Future Improvements
Real WhatsApp Cloud API integration
CRM integrations (HubSpot, Salesforce)
Lead memory & conversation tracking
Multi-user dashboard
Analytics & insights

👨‍💻 Author
Built by Ayushmaan
Final Year Computer Engineering Student
