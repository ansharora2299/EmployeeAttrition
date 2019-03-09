from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
import sqlite3
from flask_session import Session
from tempfile import mkdtemp
from helpers import login_required, sorry

app = Flask(__name__)

db = SQL("sqlite:///hr.db")
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-re-validate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@login_required
def index():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return sorry("must provide username")
        elif not request.form.get("password"):
            return sorry("must provide password")
        rows = db.execute("SELECT * FROM login WHERE username = :username", username=request.form.get("username"))
        if len(rows) != 1 or rows[0]["password"] != request.form.get("password"):
            return sorry("invalid username and/or password")
        session["user_id"] = rows[0]["id"]
        return redirect("/home")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/home")
@login_required
def home():
    return render_template("home.html")


@app.route("/view")
@login_required
def view():
    conn = sqlite3.connect("dataset.db")
    cur = conn.execute("SELECT * FROM dataset")
    # data = db1.execute("SELECT * FROM dataset")
    data = cur.fetchall()
    return render_template("view.html", data=data)


@app.route("/update")
@login_required
def update():
    return "Update Employee Details"


@app.route("/attrition")
@login_required
def attrition():
    return "Employee Attrition List"

