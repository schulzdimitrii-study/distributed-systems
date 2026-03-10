class Student:
    def __init__(self, name, email, course) -> None:
        self.__name = name
        self.__email = email
        self.__course = course
        self.__mat = None

    def set_mat(self, mat) -> None:
        self.__mat = mat

    def to_dict(self) -> dict:
        return {
            "name": self.__name,
            "email": self.__email,
            "course": self.__course,
            "mat": self.__mat
        }

