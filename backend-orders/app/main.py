from fastapi import FastAPI
from .database import Base, engine

app = FastAPI()

# Create tables on startup (if models exist later)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "OK", "message": "Orders API is running"}

from .database import Base, engine
from . import models

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

from .amazon_service import AmazonClient

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "OK", "message": "Orders API is running"}

@app.get("/amazon/orders")
def fetch_orders():
    client = AmazonClient()
    return client.get_orders()
