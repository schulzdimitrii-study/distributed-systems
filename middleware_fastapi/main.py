from app.routes.middleware import add_process_time_header
from app.routes.user import user_router
from fastapi import FastAPI

app = FastAPI()

app.middleware("http")(add_process_time_header)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"status": "ok"}
