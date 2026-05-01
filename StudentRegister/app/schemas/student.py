from pydantic import BaseModel, EmailStr

class Student(BaseModel):
    id: str
    name: str
    email: EmailStr
    course: str
    mat: int

class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    course: str | None = None

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    course: str
