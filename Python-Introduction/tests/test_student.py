from student import Student

class TestStudent:
    def test_create_student(self):
        student = Student("John Doe", "john.doe@gmail.com", "GES")
        result = student.to_dict()

        assert result["name"] == "John Doe"
        assert result["email"] == "john.doe@gmail.com"
        assert result["course"] == "GES"
        assert result["mat"] is None

    def test_set_mat(self):
        student = Student("John Doe", "john.doe@gmail.com", "GES")
        student.set_mat("GES1")

        assert student.to_dict()["mat"] == "GES1"

    def test_to_dict_returns_dict(self):
        student = Student("Alice", "alice@email.com", "GEC")
        result = student.to_dict()

        assert isinstance(result, dict)
        assert set(result.keys()) == {"name", "email", "course", "mat"}