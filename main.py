import sqlite3
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from interface_methods import *
from User import User

from forms.LoginForm import LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "matinf-secret"

con = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = con.cursor()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if user_exists(user_id):
        return User(user_id)
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        given_password = form.password.data
        password = get_password(login)
        remember_me = form.remember_me.data
        if check_user(given_password, password):
            login_user(User(get_id(login)), remember=remember_me)
            print("Success")
            return redirect("/")
        else:
            print("error")
            print(password, given_password)
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def add__user():
    if request.form['login'] not in get_logins():
        add_user(request.form['login'], request.form['password'])
    else:
        print("User already exists")
    return redirect('/')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        add_article(request.form['title'], request.form['content'])
    return render_template("index.html", get_articles=get_articles, get_comments=get_comments)


@app.route("/add_post", methods=["GET", "POST"])
@login_required
def add_post():
    add_article(request.form['title'], request.form['content'])
    return redirect('/')


@app.route("/delete_post/<int:id>", methods=["POST"])
@login_required
def delete_post(id):
    del_all_comments(id)
    del_article(id)
    return redirect('/')


@app.route("/add_comment/<int:id>", methods=["GET", "POST"])
@login_required
def add_comm(id):
    add_comment(request.form['title'], request.form['content'], id)
    return redirect('/')


@app.route("/redact_comment/<int:id>", methods=["GET", "POST"])
@login_required
def redact_comm(id):
    redact_comment(id, request.form['title'], request.form['content'])
    return redirect('/')


@app.route("/delete_comment/<int:art_id>/<int:comm_id>", methods=["POST"])
@login_required
def delete_comment(art_id, comm_id):
    del_comment(art_id, comm_id)
    return redirect('/')




app.run(port=8888)
