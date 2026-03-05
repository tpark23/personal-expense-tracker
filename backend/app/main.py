import uvicorn
from fastapi import FastAPI

from app.api.routes import router as api_router:

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)