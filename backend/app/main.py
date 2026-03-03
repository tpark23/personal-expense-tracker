import uvicorn
from fastapi import FastAPI
from routes import transactions, upload

app = FastAPI()

app.include_router(upload.router)
app.include_router(transactions.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)