from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.secret_key = 'secretkey'
app.permanent_session_lifetime = timedelta(days=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Initializes the database
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


@app.route("/")
def home():
    user = ""
    if "user" in session:
        user = session["user"]
    return f"Hello! This the main page <h1>HELLO {user}</h1>"


@app.route('/bmi_bmr_calc')
def bmi_bmr_calc():
    return render_template("bmi_bmr_calc.html")


@app.route('/bmi_bmr_results', methods=['POST'])
def bmi_bmr_results():
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    age = int(request.form['age'])
    gender = request.form['gender']
    activity_factor = float(request.form['activity'])

    bmi = 10000 * (weight / (height * height))
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = bmr * activity_factor  # Total Daily Energy Expenditure

    category = classify_bmi(bmi)
    return render_template("bmi_bmr_results.html", bmi="{:.2f}".format(bmi), category=category, bmr="{:.2f}".format(bmr), tdee="{:.2f}".format(tdee))


@app.route("/user", methods=['POST', 'GET'])
def user():
    email = None
    if "user" in session:
        username = session["user"]

        if request.method == 'POST':
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter(users.username == username).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!", "info")
        else:
            if "email" in session:
                email = session['email']

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        found_user = users.query.filter(users.username == username).first()
        found_email = users.query.filter(users.email == email).first()
        if found_user:
            flash("Username already taken", "error")
            return redirect(url_for("register"))
        elif found_email:
            flash("Email already registered with an account. Try logging in.")
            return redirect(url_for("register"))
        else:
            new_user = users(username, password, email)
            db.session.add(new_user)
            db.session.commit()
            session.permanent = True
            session["user"] = username
            session["email"] = email
            flash("Registered!", "info")
            return redirect(url_for("user"))
    else:
        return render_template("register.html")


def calculate_bmr(weight, height, age, gender):
    if gender == 'male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        found_user = users.query.filter(users.username == username).first()
        if found_user:
            found_password = found_user.password
            if found_password == password:
                session.permanent = True
                session["user"] = found_user.username
                session["email"] = found_user.email
                flash("Login Successful!", "info")
                return redirect(url_for("user"))
            else:
                flash("Wrong password", "error")
                return render_template("login.html")
        else:
            flash("Wrong username", "error")
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
