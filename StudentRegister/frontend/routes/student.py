from flask import Blueprint, flash, request, render_template, url_for, redirect
import requests

student_bp = Blueprint("student", __name__)

API_URL = "http://backend:8000/api/v1/alunos"

@student_bp.route("/cadastrar", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "course": request.form["course"]
        }
        print(data)
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for("student.list_students"))
        else:
            detail = response.json().get("detail", "Erro ao cadastrar aluno.") if response.text else "Erro ao cadastrar aluno."
            flash(detail, "danger")
    return render_template("register.html")

@student_bp.route("/", methods=["GET"])
def list_students():
    response = requests.get(API_URL)
    students = response.json() if response.ok else []
    return render_template("students.html", students=students)

@student_bp.route("/editar/<string:student_id>", methods=["GET", "POST"])
def edit(student_id):
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "course": request.form["course"]
        }
        response = requests.patch(f"{API_URL}/{student_id}", json=data)
        if response.ok:
            flash("Aluno atualizado com sucesso!", "success")
        else:
            flash("Erro ao atualizar aluno.", "danger")
        return redirect(url_for("student.list_students"))
    else:
        resp = requests.get(f"{API_URL}/{student_id}")
        student = resp.json() if resp.ok and resp.text else {}
        return render_template("update_student.html", student=student)

@student_bp.route("/delete/<string:student_id>")
def delete(student_id):
    response = requests.delete(f"{API_URL}/{student_id}")
    if response.ok:
        flash("Aluno removido com sucesso!", "success")
    else:
        flash("Erro ao remover aluno.", "danger")
    return redirect(url_for("student.list_students"))

@student_bp.route("/reset")
def reset():
    response = requests.delete(API_URL)
    if response.ok:
        flash("Banco de dados resetado com sucesso!", "info")
    else:
        flash("Erro ao resetar banco.", "danger")
    return redirect(url_for("home"))
