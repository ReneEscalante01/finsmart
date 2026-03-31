from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="FinSmart API", version = "1.0.0")

@app.get("/")
def root():
    return {"message": "FinSmart API running"}