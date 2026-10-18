with open('app/main.py', 'r', encoding='utf-8') as f:
    m = f.read()

backend_api = """
from pydantic import BaseModel
import datetime

class TxIDSubmission(BaseModel):
    amount: float
    txid: str
    client_email: str

@app.post("/api/v1/billing/submit-txid")
async def submit_txid(data: TxIDSubmission):
    # In a real app, save to a database. For now, we log it to a file.
    with open("pending_transactions.log", "a", encoding="utf-8") as log:
        log.write(f"[{datetime.datetime.now().isoformat()}] EMAIL: {data.client_email} | USDT: {data.amount} | TXID: {data.txid}\\n")
    return {"status": "success", "message": "Transaction submitted for verification"}
"""

if 'submit_txid' not in m:
    # We can inject this right before the app.get("/billing") route
    m = m.replace('@app.get("/billing"', backend_api + '\n@app.get("/billing"')
    with open('app/main.py', 'w', encoding='utf-8') as f:
        f.write(m)
    print("Backend API added!")
