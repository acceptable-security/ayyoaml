from flask import Flask, render_template, request, session, redirect, url_for
import os
from db import ayydb
from datetime import datetime

app = Flask(__name__)
db = ayydb("database.db")

# nginx ntmp callbacks
@app.route("/rtmp_callback/start")
def rtmp_start():
    return "yay"

@app.route("/rtmp_callback/end")
def rtmp_end():
    return "aww"

# Login infrmation
@app.route("/login", methods=["GET", "POST"])
def login():
    if 'session_id' in session:
        return redirect(url_for('index'))

    if request.method == "POST":
        print request.form
        username = request.form['username']
        password = request.form['password']

        session_id = db.try_login(username, password)

        if session_id is not "":
            session['session_id'] = session_id
            session['username'] = username
            return redirect(url_for('index')) # TODO - User page?
        else:
            return render_template("login.html", error="Invalid user credentials.")
    else:
        return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.pop('session_id', None)
    session.pop('username', None)
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        retypepassword = request.form['retypepassword']

        if password != retypepassword:
            return render_template("register.html", error="Please input matching passwords.")

        # TODO - Easier ask for email or forget about this
        success = db.register_user(username, username + "@ayyoa.ml", password)

        if success:
            return redirect(url_for('login'))
        else:
            return render_template("register.html", error="Unable to use those credentials to register.")
    else:
        return render_template("register.html")

# Stream stuff
@app.route("/mystream")
def mystream():
    return "wew"

@app.route("/stream/")
def empty_stream():
    return redirect(url_for("/"))

@app.route("/stream/<id>")
def stream(id):
    return "wew"

@app.route("/")
def index():
    streams = db.get_active_streams()
    to_render = []

    for stream in streams:
        idhash = stream[2]
        user = db.get_idhash(idhash)

        if not user:
            continue

        to.render_push({
            "name": stream[1],
            "streamer": user[1],
            "url": str(stream[0])
        })

    return render_template("index.html", streams=to_render)

if __name__ == "__main__":
    app.secret_key = "!Y()_{#QUPWROI:KLU!{_(UQPWO#!Y)*@#(IOUWEQJLKSA)}}"
    debug = True

    if debug:
        app.run(host = "127.0.0.1", port = 8080, debug = True)
    else:
        app.run(host = "0.0.0.0", port = 80, debug = False)
