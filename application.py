import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def navigate(destination):
    print(destination)

@app.route("/")
def index():
    # TODO: check session
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        userName = request.form.get("user-name")
        password = request.form.get("password")
        print(userName)
        print(password)
        return render_template("index.html")

    return render_template("signup.html")

@app.route("/signin", methods=["POST"])
def signin():
    userName = request.form.get("user-name")
    password = request.form.get("password")
    print(userName)
    print(password)
    return render_template("index.html")