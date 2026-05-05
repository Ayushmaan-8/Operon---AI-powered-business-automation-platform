from fastapi import FastAPI
from app.api import leads, dashboard
from app.database.session import engine, Base
from app.database import models
from app.api import webhook

from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Operon API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity in this phase
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads.router)
app.include_router(dashboard.router)
app.include_router(webhook.router)

@app.get("/health")
def health():
    return {"status": "ok"}