from fastapi import FastAPI
from routes.student import student_router

app = FastAPI(
    title="Student Register API",
    description="API para gerenciamento de alunos, desenvolvida com FastAPI. Esta documentação é atualizada automaticamente a cada mudança de código.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(student_router, prefix="/api/v1")

@app.get("/", tags=["Healthcheck"])
def read_root() -> dict:
    return {"message": "API is running! 🚀"}
