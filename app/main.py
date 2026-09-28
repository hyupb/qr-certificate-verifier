from fastapi import FastAPI

app = FastAPI(title="QR Cert Verifier")

@app.get("/")
def hello():
    return {"message": "hello"}