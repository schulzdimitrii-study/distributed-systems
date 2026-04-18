from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import APIRouter, HTTPException

user_router = APIRouter(prefix="/users", tags=["users"])

fake_db: list[User] = []

@user_router.post("/create", response_model=User, status_code=201)
def create_user(payload: UserCreate):
    nwe_id = len(fake_db) + 1
    
    if any(u.email == payload.email for u in fake_db):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(id=nwe_id, name=payload.name, email=payload.email)
    fake_db.append(user)
    return user

@user_router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((u for u in fake_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/", response_model=list[User])
def list_users():
    return fake_db

@user_router.delete("delete/{user_id}", status_code=204)
def delete_user(user_id: int):
    global fake_db
    fake_db = [u for u in fake_db if u.id != user_id]
    return None

@user_router.put("update/{user_id}", response_model=User)
def update_user(user_id: int, payload: UserCreate):
    user = next((u for u in fake_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if any(u.email == payload.email and u.id != user_id for u in fake_db):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user.name = payload.name
    user.email = payload.email
    return user
