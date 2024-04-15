import requests
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


# https://stackoverflow.com/questions/7771011/how-can-i-parse-read-and-use-json-in-python
# https://stackoverflow.com/questions/6998943/python-requests-module-json-responses?rq=3
# pip install jq
# lxml
# edamam nutrition database api
# some other palce upc

# https://spoonacular.com/food-api/docs <-- MEAL PLANS AND A FUCK TON OF STUFF
@app.route("/food_search", methods=['POST', 'GET'])
def food_search():
    food = None
    err = None
    img = None
    if request.method == 'POST':
        food = request.form['food']
        return redirect(url_for("food_search", food=food))
    else:
        if request.args.get('food'):
            foodname = request.args.get('food')
            url = f"https://api.spoonacular.com/food/ingredients/autocomplete?query={foodname}&number=1"
            r = requests.get(url)
            data = r.json()
            if data:
                item = data[0]
                food = item['name']
                img = get_image(food)
            else:
                err = "Ingredient not found!"

        return render_template("food_search.html", food=food, err=err, img=img)

def get_image(food_id=None, img_type=None):
    if isinstance(food_id, str):
        url = f"https://img.spoonacular.com/ingredients_500x500/{food_id}.jpg"
        return url
    if (isinstance(food_id, int)) and (img_type is not None):
        url = f"https://img.spoonacular.com/products/{food_id}-636x393.{img_type}"
        return url
    return None

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
