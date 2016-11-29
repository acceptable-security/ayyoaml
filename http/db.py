import sqlite3
import hashlib, binascii
import os
from datetime import datetime

class ayydb:
    def __init__(self, path="data.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.curr = self.conn.cursor()

        self.curr.execute("""CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user TEXT,
                                email TEXT,
                                password TEXT,
                                salt TEXT,
                                idhash TEXT
                             )""")

        self.curr.execute("""CREATE TABLE IF NOT EXISTS streams (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                idhash TEXT,
                                started TIMESTAMP,
                                active BOOLEAN
                             )""")

        self.curr.execute("""CREATE TABLE IF NOT EXISTS sessions (
                                token TEXT,
                                user TEXT,
                                creation TIMESTAMP,
                                length INTEGER,
                                terminated BOOLEAN
                             )""")

        self.conn.commit()

    def get_user(self, user):
        self.curr.execute("SELECT * FROM users WHERE user=?", (user,))
        return self.curr.fetchall()

    def get_email(self, email):
        self.curr.execute("SELECT * FROM users WHERE email=?", (email,))
        return self.curr.fetchall()

    def get_idhash(self, idhash):
        self.curr.execute("SELECT * FROM users WHERE idhash=?", (idhash,))
        return self.curr.fetchall()

    def register_user(self, user, email, password):
        test1 = self.get_user(user)
        test2 = self.get_email(email)

        if len(test1) != 0 or len(test2) != 0:
            return False

        salt = binascii.hexlify(os.urandom(16))
        idhash = binascii.hexlify(os.urandom(32))
        hashed = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password, salt, 100000))

        self.curr.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)", (user, email, hashed, salt, idhash))
        self.conn.commit()

        return True

    # Length is calculated in hours
    def new_session(self, user, length=24):
        timestamp = datetime.now()
        token = binascii.hexlify(os.urandom(32))

        self.curr.execute("INSERT INTO sessions VALUES (NULL, ?, ?, ?, ?)", (token, user, length, False))

        return token

    def check_session(self, token):
        self.curr.execute("SELECT * FROM sessions WHERE token=?", (token,))
        tokens = self.curr.fetchall()

        if len(tokens) != 1:
            return False

        tokens = tokens[0]
        timestamp = datetime.now()

        if tokens[3] != 0:
            if timestamp > tokens[2] + timedelta(hours=tokens[4]):
                self.curr.execute("UPDATE sessions SET terminated=1 WHERE token=?", (token,))
                self.conn.commit()
                return False

        return True

    def try_login(self, user, password, length=24):
        obj = self.get_user(user)

        if len(obj) != 1:
            return ""

        obj = obj[0]
        hashed = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password, obj[4], 100000))

        if obj[3] == hashed:
            return self.new_session(user, length=length)
        else:
            return ""

    def get_active_streams(self):
        self.curr.execute("SELECT * FROM streams WHERE active=1")
        return self.curr.fetchall()

    def start_stream(self, idhash, name):
        user = self.get_idhash(idhash)

        if len(user) != 1:
            return -1

        user = user[0]
        timestamp = datetime.now()

        self.curr.execute("INSERT INTO streams VALUES (NULL, ?, ?, ?, ?)", (name, idhash, timestamp, False))
        self.conn.commit()

        # TODO - Please god find a better way.
        self.curr.execute("SELECT * FROM streams WHERE started=?", timestamp)
        row = self.curr.fetchone()

        return row[0]

    def set_stream_active(self, id, active):
        self.curr.execute("UPDATE streams SET active=? WHERE id=?", (active, id))
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
