from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import asyncio
import os

from database import engine, get_db, Base
from models import Transaction, TransactionStatus
from schemas import WebhookRequest, TransactionResponse, HealthResponse

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Transaction Webhook Service", version="1.0.0")

# Background task
async def process_transaction_background(transaction_id: str, db_url: str):
    await asyncio.sleep(30)
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine_bg = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_bg)
    db = SessionLocal()
    try:
        transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
        if transaction:
            transaction.status = TransactionStatus.PROCESSED.value
            transaction.processed_at = datetime.utcnow()
            db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
        engine_bg.dispose()

@app.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="HEALTHY", current_time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))

@app.post("/v1/webhooks/transactions", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(webhook_data: WebhookRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        new_transaction = Transaction(
            transaction_id=webhook_data.transaction_id,
            source_account=webhook_data.source_account,
            destination_account=webhook_data.destination_account,
            amount=webhook_data.amount,
            currency=webhook_data.currency,
            status=TransactionStatus.PROCESSING.value,
            created_at=datetime.utcnow()
        )
        db.add(new_transaction)
        db.commit()
        db_url = os.getenv("DATABASE_URL")
        background_tasks.add_task(process_transaction_background, webhook_data.transaction_id, db_url)
        return {"message": "Transaction received and will be processed"}
    except IntegrityError:
        db.rollback()
        return {"message": "Transaction already received"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")

@app.get("/v1/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        source_account=transaction.source_account,
        destination_account=transaction.destination_account,
        amount=float(transaction.amount),
        currency=transaction.currency,
        status=transaction.status,
        created_at=transaction.created_at,
        processed_at=transaction.processed_at
    )
