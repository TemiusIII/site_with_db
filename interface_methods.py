import sqlite3

from werkzeug.security import check_password_hash

con = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = con.cursor()


def get_articles():
    return cur.execute("SELECT * FROM Article").fetchall()


def get_comments(arr):
    return cur.execute("SELECT * FROM Comment WHERE Article_id = ?", (arr[0],)).fetchall()


def add_article(title, content):
    cur.execute("INSERT INTO Article(title, content) VALUES (?, ?);", (title, content))
    get_articles()
    con.commit()


def del_article(id):
    cur.execute('''DELETE FROM Article 
                WHERE id = ?;''', (id,))
    con.commit()
    get_articles()


def add_comment(title, content, id):
    cur.execute('''INSERT INTO Comment(title, content, Article_id)
                    VALUES (?,?,?)''', (title, content, id))
    con.commit()


def redact_comment(id, title, content):
    cur.execute('''UPDATE Comment
                   SET title = ? WHERE id = ?''', (title, id))
    cur.execute('''UPDATE Comment
                   SET content = ? WHERE id = ?''', (content, id))
    con.commit()


def del_comment(id, comm_id):
    cur.execute('''DELETE FROM Comment
                    WHERE id = ? AND Article_id == ?''', (comm_id, id))
    con.commit()


def del_all_comments(id):
    cur.execute('''DELETE FROM Comment
                    WHERE Article_id == ?''', (id,))
    con.commit()


def check_user(given_password, password):
    return check_password_hash(given_password, password)


def get_login(id):
    return con.execute('''SELECT * FROM Users)
                    WHERE id = ?''', (id,)).fetchone()
