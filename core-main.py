from fastapi import FastAPI, BackgroundTasks, HTTPException
from datetime import datetime
import asyncio

app = FastAPI()

async def process_transaction(transaction_id: str, data: dict):
    # Update status to PROCESSING
    await asyncio.sleep(30)  # 30-second delay
    # Update status to PROCESSED with processed_at timestamp

@app.post("/v1/webhooks/transactions", status_code=202)
async def webhook(transaction: dict, background_tasks: BackgroundTasks):
    # Try to insert with transaction_id (will fail if duplicate)
    # Add background task if insert successful
    background_tasks.add_task(process_transaction, transaction["transaction_id"], transaction)
    return {}

@app.get("/")
async def health():
    return {"status": "HEALTHY", "current_time": datetime.utcnow().isoformat() + "Z"}

@app.get("/v1/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    # Query DB and return transaction
    pass
