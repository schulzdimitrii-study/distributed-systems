from app.schemas.student import StudentCreate, Student, StudentUpdate
from app.services.student_service import StudentService
from fastapi import APIRouter, HTTPException

student_router = APIRouter(prefix="/alunos", tags=["Alunos"])

service = StudentService()

@student_router.post("/", response_model=Student, status_code=201)
async def create_student(payload: StudentCreate) -> Student:
    return await service.create_student(payload)

@student_router.get("/{student_id}", response_model=Student)
async def get_student(student_id: str) -> Student:
    try:
        student = await service.get_student(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@student_router.get("/", response_model=list[Student])
async def list_students() -> list[Student]:
    return await service.get_students()

@student_router.patch("/{student_id}", response_model=Student)
async def update_student(student_id: str, payload: StudentUpdate) -> Student:
    try:
        student = await service.update_student(student_id, payload)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@student_router.delete("/{student_id}", status_code=204)
async def delete_student(student_id: str) -> None:
    try:
        success = await service.delete_student(student_id)
        if not success:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@student_router.delete("/", status_code=204)
async def reset_students() -> None:
    await service.reset_students()
