from src.student import Student
from src.university import university

def main():
    while True:
        print(
            "--- Menu Acadêmico --- \
            \n 1 - Matricular aluno \
            \n 2 - Ver aluno \
            \n 3 - Ver lista de alunos \
            \n 4 - Modificar dados do Aluno \
            \n 5 - Remover aluno \
            \n 0 - Sair "
        )
        choice = input()

        match choice:
            case "1":
                print("--- Insira as informações do aluno ---")
                name = input("Nome: ")
                email = input("Email: ")
                print("Cursos disponíveis:")
                for course in university.get_courses():
                    print(f"{course['name']} ({course['code']})")
                course = input("Curso: ")

                new_student = Student(name, email, course)
                university.add_student(new_student)

                print("Aluno matriculado com sucesso!")
                print(new_student.to_dict())

            case "2":
                name = input("Insira o nome do aluno: ")
                student = university.get_student(name)
                print(student)

            case "3":
                students = university.get_students()
                print(students)

            case "4":
                selected = input("Insira o nome do aluno que deseja modificar: ")
                print("Insira os novos dados do aluno (deixe em branco para não modificar):")
                name = input("Nome: ")
                email = input("Email: ")
                course = input("Curso: ")

                updated_student = university.update_student(selected, name, email, course)
                print(updated_student)

            case "5":
                name = input("Insira o nome do aluno que deseja remover: ")
                university.remove_student(name)

                print("Aluno removido com sucesso!")

            case "0":
                print("Saindo...")
                break

            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
