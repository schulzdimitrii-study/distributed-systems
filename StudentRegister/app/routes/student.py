from app.schemas.student import StudentCreate, Student, StudentUpdate
from app.services.studentService import StudentService
from fastapi import APIRouter, HTTPException

student_router = APIRouter(prefix="/alunos", tags=["alunos"])

service = StudentService()

@student_router.post("/", response_model=Student, status_code=201)
def create_student(payload: StudentCreate):
    return service.create_student(payload)

@student_router.get("/{student_id}", response_model=Student)
def get_student(student_id: str):
    student = service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@student_router.get("/", response_model=list[Student])
def list_students():
    return service.get_students()

@student_router.patch("/{student_id}", response_model=Student)
def update_student(student_id: str, payload: StudentUpdate):
    student = service.update_student(student_id, payload)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@student_router.delete("/{student_id}", status_code=204)
def delete_student(student_id: str):
    success = service.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")

@student_router.delete("/", status_code=204)
def reset_students():
    service.reset_students()
