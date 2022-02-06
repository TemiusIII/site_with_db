import sqlite3
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from interface_methods import *

from forms.LoginForm import LoginForm

app = Flask(__name__)
con = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = con.cursor()



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        add_article(request.form['title'], request.form['content'])
    return render_template("index.html", get_articles=get_articles, get_comments=get_comments)


@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    add_article(request.form['title'], request.form['content'])
    return redirect('/')


@app.route("/delete_post/<int:id>", methods=["POST"])
def delete_post(id):
    del_all_comments(id)
    del_article(id)
    return redirect('/')


@app.route("/add_comment/<int:id>", methods=["GET", "POST"])
def add_comm(id):
    add_comment(request.form['title'], request.form['content'], id)
    return redirect('/')


@app.route("/redact_comment/<int:id>", methods=["GET", "POST"])
def redact_comm(id):
    redact_comment(id, request.form['title'], request.form['content'])
    return redirect('/')


@app.route("/delete_comment/<int:art_id>/<int:comm_id>", methods=["POST"])
def delete_comment(art_id, comm_id):
    del_comment(art_id, comm_id)
    return redirect('/')


app.run(port=8888)
