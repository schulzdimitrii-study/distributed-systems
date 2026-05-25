from schemas.student import Student, StudentCreate, StudentUpdate
from db.connection import get_connection
import re


class StudentService:
    def __init__(self) -> None:
        self.course_sequences: dict[str, int] = {}

    async def create_student(self, student_data: StudentCreate) -> Student:
        conn = await get_connection()
        
        try:
            course = student_data.course.upper()
            mat = self.__get_next_mat(course)
            student_id = f"{course}{mat}"

            await conn.execute(
                "INSERT INTO students (name, email, course, mat) VALUES ($1, $2, $3, $4)",
                student_data.name,
                student_data.email,
                course,
                mat
            )

            return Student(
                id=student_id,
                name=student_data.name,
                email=student_data.email,
                course=course,
                mat=mat
            )
        finally:
            await conn.close()
    
    def __get_next_mat(self, course: str) -> int:
        if course not in self.course_sequences:
            self.course_sequences[course] = 1
        else:
            self.course_sequences[course] += 1
        return self.course_sequences[course]
    
    async def reset_students(self) -> None:
        conn = await get_connection()
        try:
            await conn.execute("TRUNCATE students RESTART IDENTITY")
            self.course_sequences.clear()
        finally:
            await conn.close()

    async def get_students(self) -> list[Student]:
        conn = await get_connection()
        
        try:
            rows = await conn.fetch("SELECT id, name, email, course, mat FROM students ORDER BY id")
            return [
                Student(
                    id=f"{row['course']}{row['mat']}",
                    name=row['name'],
                    email=row['email'],
                    course=row['course'],
                    mat=row['mat']
                )
                for row in rows
            ]
        finally:
            await conn.close()
        
    
    async def get_student(self, student_id: str) -> Student | None:
        conn = await get_connection()
        
        try:
            course, mat = self.__split_student_id(student_id)
            http_response = await conn.fetchrow(
                "SELECT id, name, email, course, mat FROM students WHERE course = $1 AND mat = $2",
                course,
                mat
            )
            if http_response:
                return Student(
                    id=f"{http_response['course']}{http_response['mat']}",
                    name=http_response['name'],
                    email=http_response['email'],
                    course=http_response['course'],
                    mat=http_response['mat']
                )
            return None
        finally:            
            await conn.close()
    
    async def update_student(self, student_id: str, student_data: StudentUpdate) -> Student | None:
        conn = await get_connection()
        
        try:
            course, mat = self.__split_student_id(student_id)
            student = await conn.fetchrow(
                "SELECT id, name, email, course, mat FROM students WHERE course = $1 AND mat = $2",
                course,
                mat
            )
            if not student:
                return None
            
            updated_name = student_data.name if student_data.name else student["name"]
            updated_email = student_data.email if student_data.email else student["email"]
            updated_course = student_data.course.upper() if student_data.course else student["course"]
            
            await conn.execute(
                "UPDATE students SET name = $1, email = $2, course = $3 WHERE course = $4 AND mat = $5",
                updated_name,
                updated_email,
                updated_course,
                course,
                mat
            )
            
            return Student(
                id=f"{updated_course}{student['mat']}",
                name=updated_name,
                email=updated_email,
                course=updated_course,
                mat=student["mat"]
            )
        finally:
            await conn.close()
    
    async def delete_student(self, student_id: str) -> bool:
        conn = await get_connection()
        
        try:
            course, mat = self.__split_student_id(student_id)
            http_response = await conn.execute("DELETE FROM students WHERE course = $1 AND mat = $2", course, mat)
            return http_response == "DELETE 1"
        finally:
            await conn.close()

    def __split_student_id(self, student_id: str) -> tuple[str, int]:
        match = re.match(r"^([A-Za-z]+)(\d+)$", student_id)
        if not match:
            raise ValueError("Invalid student id format")
        return match.group(1).upper(), int(match.group(2))


service = StudentService()