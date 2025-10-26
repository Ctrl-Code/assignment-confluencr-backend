from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WebhookRequest(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str

class TransactionResponse(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    status: str
    current_time: str
