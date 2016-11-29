from flask import Flask, render_template, request
import os
from db import ayydb

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
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        session_id = db.check_login(username, password)

        if session_id is not "":
            session.session_id = session_id
            return redirect(url_for('index')) # TODO - User page?
        else:
            return render_template("login.html", error="Invalid user credentials.")
    else:
        return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.pop('session_id', None)
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return "no"
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
    return render_template("index.html", streams = [
        { "name": "Test", "streamer": "Brian", "url": "weiner" },
        { "name": "Test", "streamer": "[]----[]", "url": "weiner" },
        { "name": "Test", "streamer": "Your face", "url": "weiner" },
        { "name": "Test", "streamer": "jK!", "url": "weiner" }
    ])

if __name__ == "__main__":
    app.secret_key = "!Y()_{#QUPWROI:KLU!{_(UQPWO#!Y)*@#(IOUWEQJLKSA)}}"
    debug = True

    if debug:
        app.run(host = "127.0.0.1", port = 8080, debug = True)
    else:
        app.run(host = "0.0.0.0", port = 80, debug = False)
