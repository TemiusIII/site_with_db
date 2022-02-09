import sqlite3

from flask_login import UserMixin
from werkzeug.security import check_password_hash

con = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = con.cursor()


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.login = User.get_login(self)
        self.password = User.get_password(self)

    def get_login(self):
        return cur.execute('''SELECT login FROM Users
                        WHERE id = ?''', (self.id,)).fetchone()[0]

    def get_password(self):
        return cur.execute('''SELECT password FROM Users
                                WHERE login = ?''', (self.login,)).fetchone()[0]

    def check_user(self, password):
        return check_password_hash(self.password, password)
