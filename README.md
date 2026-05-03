\# Operon – AI-Powered Business Automation Platform


\##  Overview

Operon is an AI-powered system that:
\- Captures leads
\- Analyzes intent using LLMs
\- Scores lead quality
\- Triggers automated actions
\- Displays insights via dashboard


\##  Features

\- Lead ingestion (form/API)
\- AI lead analysis (Groq LLM)
\- Action engine (follow-up, ignore, etc.)
\- Dashboard (Next.js)
\- Logging \& monitoring


\## Tech Stack

\- Backend: FastAPI, SQLAlchemy
\- AI: Groq API
\- Frontend: Next.js, Tailwind
\- Database: SQLite (dev)


\## Setup

\### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

\### Frontend
```bash
cd frontend/nextjs-dashboard
npm install
npm run dev

Deployment
Backend: Render
Frontend: Vercel

Author: Ayushmaan

