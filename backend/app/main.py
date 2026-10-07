from fastapi import FastAPI

app = FastAPI(title="Quest Me API")

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Quest Me API is running"}
