CREATE TABLE transactions (
    transaction_id VARCHAR PRIMARY KEY,
    source_account VARCHAR NOT NULL,
    destination_account VARCHAR NOT NULL,
    amount DECIMAL NOT NULL,
    currency VARCHAR NOT NULL,
    status VARCHAR NOT NULL,  -- 'PROCESSING' or 'PROCESSED'
    created_at TIMESTAMP NOT NULL,
    processed_at TIMESTAMP
);
