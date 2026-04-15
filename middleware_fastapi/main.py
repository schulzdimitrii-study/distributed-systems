from app.routes.user import user_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(user_router)

@app.get("/")
def read_root():
    return {"status": "ok"}
