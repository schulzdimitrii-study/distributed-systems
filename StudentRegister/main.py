from fastapi import FastAPI
from app.routes.student import student_router

app = FastAPI()

app.include_router(student_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "ok"}
