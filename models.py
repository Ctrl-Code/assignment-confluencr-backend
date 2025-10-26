from sqlalchemy import Column, String, Numeric, DateTime
from database import Base
from datetime import datetime
import enum

class TransactionStatus(str, enum.Enum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(String, primary_key=True, index=True)
    source_account = Column(String, nullable=False)
    destination_account = Column(String, nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    currency = Column(String, nullable=False)
    status = Column(String, nullable=False, default=TransactionStatus.PROCESSING.value)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
