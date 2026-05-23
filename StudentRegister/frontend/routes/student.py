from flask import Blueprint, flash, request, render_template, url_for, redirect
import requests

student_bp = Blueprint("student", __name__)

API_URL = "http://backend:8000/api/v1/alunos"

@student_bp.route("/cadastro", methods=["POST"])
def register():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "course": request.form["course"]
        }
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for("alunos"))
        else:
            flash(response.json().get("detail", "Erro ao cadastrar professor."), "danger")
    return render_template("register.html")

@student_bp.route("/alunos")
def students():
    response = requests.get(API_URL)
    students = response.json() if response.ok else []
    return render_template("students.html", students=students)

@student_bp.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit(student_id):
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "course": request.form["course"]
        }
        response = requests.patch(f"{API_URL}/{student_id}", json=data)
        if response.ok:
            flash("Professor atualizado com sucesso!", "success")
        else:
            flash("Erro ao atualizar professor.", "danger")
        return redirect(url_for("professores"))
    else:
        student = requests.get(f"{API_URL}/{student_id}").json()
        return render_template("editar.html", professor=student)

@student_bp.route("/delete/<int:student_id>")
def delete(student_id):
    response = requests.delete(f"{API_URL}/{student_id}")
    if response.ok:
        flash("Professor removido com sucesso!", "success")
    else:
        flash("Erro ao remover professor.", "danger")
    return redirect(url_for("professores"))

@student_bp.route("/reset")
def reset():
    response = requests.delete(API_URL)
    if response.ok:
        flash("Banco de dados resetado com sucesso!", "info")
    else:
        flash("Erro ao resetar banco.", "danger")
    return redirect(url_for("home"))
