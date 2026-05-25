
from flask import Flask, render_template
from routes.student import student_bp

app = Flask(__name__)
app.secret_key = "secret"

app.register_blueprint(student_bp, url_prefix="/alunos")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
