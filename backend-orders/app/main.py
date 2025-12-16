from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from .database import Base, engine, SessionLocal
from app.amazon.client import AmazonClient
from .crud import upsert_amazon_order

app = FastAPI()

# Create tables (safe if they already exist)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "OK", "message": "Orders API is running"}


@app.get("/amazon/orders")
def fetch_orders(db: Session = Depends(get_db)):
    client = AmazonClient()

    # Pull last 3 days of UPDATED orders
    last_updated_after = datetime.now(timezone.utc) - timedelta(days=3)

    payload = client.get_orders(last_updated_after)
    orders = payload.get("Orders", [])

    for o in orders:
        upsert_amazon_order(
            db=db,
            marketplace_code="amazon_us",
            amazon_order_id=o["AmazonOrderId"],
            status=o["OrderStatus"],
            order_date=datetime.fromisoformat(
                o["PurchaseDate"].replace("Z", "+00:00")
            ),
            buyer_email=o.get("BuyerInfo", {}).get("BuyerEmail"),
            total_amount=float(o["OrderTotal"]["Amount"])
            if o.get("OrderTotal")
            else None,
            currency=o["OrderTotal"]["CurrencyCode"]
            if o.get("OrderTotal")
            else "USD",
        )

    return {
        "orders_received": len(orders),
        "status": "success"
    }
