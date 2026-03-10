from src.student import Student


class __University:

    def __init__(self) -> None:
        self.__students = []
        self.__courses = [
            {"name": "Engenharia de Software", "code": "GES", "count": 0},
            {"name": "Engenharia de Produção", "code": "GEP", "count": 0},
            {"name": "Engenharia de Telecomunicações", "code": "GET", "count": 0},
            {"name": "Engenharia de Controle e Automação", "code": "GEA", "count": 0},
            {"name": "Engenharia Elétrica", "code": "GEL", "count": 0},
            {"name": "Engenharia de Computação", "code": "GEC", "count": 0},
        ]

    def add_student(self, student: Student) -> None:
        course_code = student.to_dict()["course"]
        mat = self.generate_mat(course_code)
        if mat is None:
            print("Curso não encontrado.")
            return
        student.set_mat(mat)
        self.__students.append(student)

    def get_students(self) -> list[Student]:
        students_list = []
        for student in self.__students:
            students_list.append(student.to_dict())
        return students_list

    def get_student(self, name: str) -> dict:
        for student in self.__students:
            if name in student.to_dict()["name"]:
                return student.to_dict()
        return {"message": "Aluno não encontrado"}

    def update_student(self, selected, name=None, email=None, course=None) -> dict:
        student = self.get_student(selected)

        if name:
            student["name"] = name
        if email:
            student["email"] = email
        if course:
            student["course"] = course

        return student

    def remove_student(self, name: str) -> None:
        for student in self.__students:
            if name in student.to_dict()["name"]:
                self.__students.remove(student)
                return

    def get_courses(self) -> list[dict[str, str]]:
        return self.__courses

    def generate_mat(self, course_code: str) -> str | None:
        try:
            for course in self.__courses:
                if course["code"] == course_code.strip().upper():
                    course["count"] += 1
                    return course["code"] + str(course["count"])
        except Exception as e:
            print("Erro ao gerar matrícula:", e)
            return ""

    def reset(self) -> None:
        self.__students.clear()
        for course in self.__courses:
            course["count"] = 0


university = __University()