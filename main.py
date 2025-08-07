import uvicorn
from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.utils import router as utils_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(utils_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)