import sqlite3
import hashlib, binascii
import os

class ayydb:
    def __init__(self, path="data.db"):
        self.conn = sqlite3.connect(path)
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
                                termination TIMESTAMP,
                                terminated BOOLEAN
                             )""")

        self.conn.commit()

    def get_user(user):
        self.curr.execute("SELECT * FROM users WHERE user=?", (user,))
        return self.curr.fetchall()

    def get_email(email):
        self.curr.execute("SELECT * FROM users WHERE email=?", (email,))
        return self.curr.fetchall()

    def get_idhash(idhash):
        self.curr.execute("SELECT * FROM users WHERE idhash=?", (idhash,))
        return self.curr.fetchall()

    def register_user(user, email, password):
        test1 = self.get_user(user)
        test2 = self.get_email(email)

        if len(test1) != 0 or len(test2) != 0:
            return False

        salt = binascii.hexlify(os.urandom(16))
        idhash = binascii.hexlify(os.urandom(32))
        hashed = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password, salt, 100000))

        self.curr.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user, email, hashed, salt, idhash))
        self.conn.commit()

        return True

    # Length is calculated in hours
    def new_session(user, length=24):
        timestamp = datetime.now()
        token = binascii.hexlify(os.urandom(32))
        end = timestamp + timedelta(hours=length)

        this.curr.execute("INSERT INTO sesions VALUES (?, ?, ?, ?)", (token, user, timestamp, end))

        return token

    def try_login(user, password, length=24):
        obj = self.get_user(user)

        if len(obj) != 1:
            return ""

        obj = obj[0]
        hashed = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password, obj[4], 100000))

        if obj[3] == hashed:
            return this.new_session(user, length=length)
        else:
            return ""

    def get_active_streams():
        self.conn.execute("SELECT * FROM streams WHERE active=1")
        return self.curr.fetchall()

    def start_stream(idhash, name):
        user = self.get_idhash(idhash)

        if len(user) != 1:
            return -1

        user = user[0]
        timestamp = datetime.now()

        self.curr.execute("INSERT INTO streams VALUES (?, ?, ?, ?)", (name, idhash, timestamp, False))
        self.conn.commit()

        # TODO - Please god find a better way.
        self.curr.execute("SELECT * FROM streams WHERE started=?", timestamp)
        row = self.curr.fetchone()

        return row[0]

    def set_stream_active(id, active):
        self.curr.execute("UPDATE streams SET active=? WHERE id=?", (active, id))
        self.conn.commit()

    def close():
        self.conn.commit()
        self.conn.close()
