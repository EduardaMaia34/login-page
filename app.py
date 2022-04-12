from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3


banco = sqlite3.connect("contas.db" , check_same_thread=False)
cursor = banco.cursor()

app = Flask("__name__")

app.secret_key = "app.secret_key.project=loginwithflask"

nome = None
email = None
senha = None

@app.route("/", methods=["GET","POST"])
def index():
    return redirect(url_for("login_page"))


@app.route("/criarconta", methods=["POST", "GET"])
def criar_page():
    return render_template("criarconta.html")


@app.route("/criarconta-process", methods = ["POST", "GET"])

def criar_conta():

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")

    cursor.execute("SELECT email FROM contas WHERE email=?", (email,))
    res = cursor.fetchall()

    if res == []:
        cursor.execute("INSERT INTO contas VALUES (?,?,?)", (nome, email, senha))
        banco.commit()
        return redirect(url_for("login_page"))

    else:
       return render_template ("criarconta.html", error="Já existe uma conta com esse email")

@app.route("/login", methods=["POST", "GET"])
def login_page():
    return render_template("login.html", error="")


@app.route("/login-process", methods=["POST", "GET"])
def login():
    email = request.form.get("email")
    senha = request.form.get("senha")
    
    cursor.execute("SELECT nome FROM contas WHERE email=? and password=?", (email, senha))
    res = cursor.fetchall()

    if res == []:
        return render_template("login.html", error="Cadastro não existe")
    else:
        if request.method == "POST": #Se já não está login
            user = request.form['email']
            session["user"] = user
            return redirect(url_for("conta"))


@app.route("/conta", methods=["POST", "GET"])
def conta():
    if "user" in session:
        user = session["user"]

        cursor.execute("SELECT nome FROM contas WHERE email=?", (user,))
        nome = cursor.fetchall()

        return render_template("conta.html", nome=nome)
    else:
        return redirect(url_for("login_page"))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True)