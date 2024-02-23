from flask import Flask, redirect, url_for, render_template, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello! This the main page <h1>HELLO<h/1>"


@app.route("/<name>")
def user(name):
    return f"Hello {escape(name)}!"


@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin"))


@app.route("/index")
def index():
    return render_template("./templates/index.html")


if __name__ == "__main__":
    app.run(debug=True)
