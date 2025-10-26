# Transaction Webhook Service

**Disclaimer:**  
If you are testing this on free cloud platforms like Render, **please visit `/redoc` or `/docs` in your browser before making any API calls**. Free services may put your app to sleep when idle, causing endpoints to hang or appear down; opening the documentation page wakes up the app. If you find requests timing out or getting no response, the likely reason is the free server was sleeping. Wait ~30 seconds after waking, then retry your tests.

---

FastAPI-based webhook service for processing financial transactions with idempotency support and background processing.

---

## Quick Start

### Prerequisites
- Python 3.8 up to Python 3.12 (Python 3.13 is not supported due to SQLAlchemy compatibility)
- Supabase account (free tier works)
- Git

### Installation

1. **Clone this repo**
    ```
    git clone https://github.com/<your-username>/transaction-webhook-service.git
    cd transaction-webhook-service
    ```

2. **Create virtual environment**
    ```
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Set up Supabase**
    - Create a new project
    - Go to Project → Settings → Database
    - Copy your connection string (PostgreSQL URI)
    - Put it in a `.env` file:
      ```
      DATABASE_URL=postgresql://postgres:<your-password>@db.xxxxx.supabase.co:5432/postgres
      ```

5. **Run**
    ```
    uvicorn main:app --reload
    ```
    Visit http://localhost:8000/docs for auto-generated API docs.

---

## How to Test

You can use Swagger UI (`/docs`) or cURL:

- **Health check**
    ```
    curl http://localhost:8000/
    ```
- **Webhook endpoint (POST /v1/webhooks/transactions)**
    ```
    curl -X POST http://localhost:8000/v1/webhooks/transactions \
      -H "Content-Type: application/json" \
      -d '{"transaction_id":"txn_test001","source_account":"uA","destination_account":"mB","amount":1000,"currency":"INR"}'
    ```
- **Check transaction status**
    ```
    curl http://localhost:8000/v1/transactions/txn_test001
    ```

### If running on free cloud (e.g., Render)
- Always open `/redoc` or `/docs` page first to wake up the service if it was idle.
- If requests do not respond, wait for the server to start and try again.

---

## Technical Choices

- **FastAPI:** Quick to build, async support, and built-in docs.
- **Supabase/Postgres:** Managed, zero-config, can see/test data easily.
- **SQLAlchemy:** Use Python for DB schema, less error-prone.
- **BackgroundTasks:** Good for demo; recommend Celery for high scale/production.

---

## What this service can do

- Accept webhooks and process them after a 30 second delay
- Keep only one transaction per transaction_id (idempotency)
- Query transaction status
- Check service health

---

*Demo/assignment only; for big production jobs, switch to proper background worker/task queue.*

**Author:** Vipul Singh Thakur (ctrl-code)
