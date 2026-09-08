from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ethiobank_receipts import extract_receipt

app = FastAPI(title="EthioBank Receipts API")

# 1. ይህ የ CORS ችግርን 100% ይፈታል (Failed to fetch እንዳይል ያደርጋል)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ከማንኛውም Frontend ይቀበላል
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReceiptRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "EthioBank Receipts API is successfully running!"}

@app.post("/extract")
def process_receipt(data: ReceiptRequest):
    try:
        # URL ውስጥ ክፍተት (Space) ካለ ያጠፋል
        clean_url = data.url.strip()
        
        result = extract_receipt(clean_url)
        return {"status": "success", "data": result}
    except Exception as e:
        # ችግር ካጋጠመ ትክክለኛውን የስህተት መልእክት ይመልሳል
        raise HTTPException(status_code=400, detail=str(e))
