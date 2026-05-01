from app.schemas.student import Student

class StudentService:
    def __init__(self) -> None:
        self.students = []
        self.course_sequences = {}

    def create_student(self, student_data) -> Student:
        course = student_data.course.upper()
        if course not in self.course_sequences:
            self.course_sequences[course] = 1
        else:
            self.course_sequences[course] += 1
            
        mat = self.course_sequences[course]
        student_id = f"{course}{mat}"
        
        student = {
            "id": student_id,
            "name": student_data.name,
            "email": student_data.email,
            "course": course,
            "mat": mat
        }
        self.students.append(student)
        return student

    def get_students(self) -> list[Student]:
        return self.students
    
    def get_student(self, student_id: str) -> Student:
        for student in self.students:
            if student["id"] == student_id:
                return student
        return None
    
    def update_student(self, student_id: str, student_data) -> Student:
        for student in self.students:
            if student["id"] == student_id:
                if student_data.name:
                    student["name"] = student_data.name
                if student_data.email:
                    student["email"] = student_data.email
                if student_data.course:
                    student["course"] = student_data.course.upper()
                return student
        return None
    
    def delete_student(self, student_id: str) -> bool:
        for i, student in enumerate(self.students):
            if student["id"] == student_id:
                del self.students[i]
                return True
        return False

    def reset_students(self) -> None:
        self.students = []
        self.course_sequences = {}
    
    def delete_students(self) -> None:
        self.students.clear()
        self.next_id = 1
        self.course_sequences.clear()