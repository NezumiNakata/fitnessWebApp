from flask import Flask, redirect, url_for, render_template, request
from markupsafe import escape


app = Flask(__name__)

users = {
        'admin': '12345',
        'drewPeacock': '12345'
        }


@app.route("/")
def home():
    return "Hello! This the main page <h1>HELLO<h/1>"


@app.route("/<name>")
def user(name):
    return f"Hello {escape(name)}!"


@app.route("/login_page")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        if username in users and users[username] == password:
            return user(username)
        else:
            return '<h1>Invalid Credentials</h1>'
    else:
        return login_page()


@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin"))


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
