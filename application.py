import os
import uuid

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from models import User

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# hashing function
import hashlib
def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))

def navigate(destination):
    print(destination)

@app.route("/")
def index():
    # TODO: check session
    if 'username' in session and session['username'] is not "":
        user_name = session['username']
        return render_template("search.html", username=user_name)

    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            db = db_session()
            user_name = request.form.get("user-name")
            password = request.form.get("password")
            hashed = encrypt_string(password)

            newUser = User(id=str(uuid.uuid4()), username=user_name, password=str(hashed))
            db.add(newUser)
            db.commit()
            print('Success to create user')
        except:
            db.rollback()
            return render_template("error.html", error_message="Failed to signup user")

        return render_template("success.html", success_message="Success to signup!")

    return render_template("signup.html")

@app.route("/signin", methods=["POST"])
def signin():

    try:
        db = db_session()
        user_name = request.form.get("user-name")
        password = request.form.get("password")
        hashed = encrypt_string(password)
        user = db.query(User).filter_by(username=user_name, password=str(hashed)).first()
        session['username'] = user_name
    except:
        return render_template("error.html", error_message="Failed to signin")

    return render_template("search.html", username=user_name)

@app.route("/signout")
def signout():
    session['username'] = ""
    return render_template("success.html", success_message="Success to Signed out!")
