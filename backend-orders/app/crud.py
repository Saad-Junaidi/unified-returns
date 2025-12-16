from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .models import Order, Marketplace


def upsert_amazon_order(
    db: Session,
    marketplace_code: str,
    amazon_order_id: str,
    status: str,
    order_date: datetime,
    buyer_email: str | None,
    total_amount: float | None,
    currency: str,
):
    marketplace = (
        db.query(Marketplace)
        .filter(Marketplace.code == marketplace_code)
        .first()
    )

    if not marketplace:
        marketplace = Marketplace(
            code=marketplace_code,
            name="Amazon US"
        )
        db.add(marketplace)
        db.commit()
        db.refresh(marketplace)

    order = (
        db.query(Order)
        .filter(Order.amazon_order_id == amazon_order_id)
        .first()
    )

    if order:
        order.status = status
        order.order_date = order_date
        order.buyer_email = buyer_email
        order.total_amount = total_amount
        order.currency = currency
    else:
        order = Order(
            marketplace_id=marketplace.id,
            amazon_order_id=amazon_order_id,
            status=status,
            order_date=order_date,
            buyer_email=buyer_email,
            total_amount=total_amount,
            currency=currency,
            created_at=datetime.now(timezone.utc),
        )
        db.add(order)

    db.commit()
