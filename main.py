from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ethiobank_receipts import extract_receipt

app = FastAPI(title="EthioBank Receipts API")

class ReceiptRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "EthioBank Receipts API is running successfully!"}

@app.post("/extract")
def process_receipt(data: ReceiptRequest):
    try:
        result = extract_receipt(data.url)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
