import pytest
from src.student import Student
from unittest.mock import Mock
from src.university import university

class MockStudent:
    def _make_mock_student(self, name="John Doe", email="john.doe@gmail.com", course="GES", mat=None):
        """Cria um mock de Student para isolar University."""
        student = Mock(spec=Student)
        student_dict = {"name": name, "email": email, "course": course, "mat": mat}

        def set_mat_side_effect(m):
            student_dict["mat"] = m

        student.set_mat = Mock(side_effect=set_mat_side_effect)
        student.to_dict = Mock(return_value=student_dict)

        student.name = name
        student.email = email
        student.course = course

        return student, student_dict

class TestUniversity():
    @pytest.fixture(autouse=True)
    def clean_university(self):
        university.reset()

    def test_add_student(self):
        mock = MockStudent()
        student, student_dict = mock._make_mock_student()

        university.add_student(student)

        student.set_mat.assert_called_once()
        assert student_dict["mat"] == "GES1"
        assert len(university.get_students()) == 1

    def test_get_students(self):
        mock = MockStudent()
        student, _ = mock._make_mock_student()
        university.add_student(student)

        students = university.get_students()
        assert len(students) == 1
        assert students[0]["name"] == "John Doe"

    def test_get_student_found(self):
        mock = MockStudent()
        student, _ = mock._make_mock_student()
        university.add_student(student)

        result = university.get_student("John Doe")

        assert result["name"] == "John Doe"
        assert result["mat"] == "GES1"

    def test_get_student_not_found(self):
        result = university.get_student("Jane Doe")
        assert result == {"message": "Aluno não encontrado"}

    def test_update_student(self):
        mock = MockStudent()
        student, _ = mock._make_mock_student()
        university.add_student(student)

        updated = university.update_student("John Doe", name="John Smith")

        assert updated["name"] == "John Smith"

    def test_remove_student(self):
        mock = MockStudent()
        student, _ = mock._make_mock_student()
        university.add_student(student)

        university.remove_student("John Doe")

        assert university.get_student("John Doe") == {"message": "Aluno não encontrado"}
