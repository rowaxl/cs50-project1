import os
import uuid
import sys

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from models import User, Book

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

search_options = [
    {'label': "Title", 'value': "title"},
    {'label': "Author", 'value': "author"},
    {'label': "Year", 'value': "year"},
    {'label': "ISBN", 'value': "isbn"}]

def navigate(destination):
    print(destination)

@app.route("/")
def index():
    if 'username' in session and session['username'] is not "":
        user_name = session['username']
        return render_template(
            "search.html",
            username=user_name,
            search_options=search_options,
            found=False,
        )

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
            e = sys.exc_info()[0]
            print(f"error: {e}")
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
        e = sys.exc_info()[0]
        print(f"error: {e}")
        return render_template("error.html", error_message="Failed to signin")

    return render_template(
            "search.html",
            username=user_name,
            search_options=search_options,
            found=False,
        )

@app.route("/signout")
def signout():
    session['username'] = ""
    return render_template("success.html", success_message="Success to Signed out!")

@app.route("/search")
def search():
    if 'username' in session and session['username'] is not "":
        try:
            category = request.args.get('category')
            query = request.args.get('query')

            if not category or not query:
                return render_template("search.html",
                    username=session['username'],
                    search_options=search_options)

            db = db_session()
            if category == "title":
                books = db.query(Book).filter(Book.title.like(f"%{query}%")).all()
            elif category == "isbn":
                books = db.query(Book).filter(Book.isbn.like(f"%{query}%")).all()
            elif category == "author":
                books = db.query(Book).filter(Book.author.like(f"%{query}%")).all()
            elif category == "year":
                books = db.query(Book).filter(Book.year == query).all()

            return render_template("search.html",
                    username=session['username'],
                    search_options=search_options,
                    found=True,
                    count=len(books),
                    books=books
                )
        except:
            e = sys.exc_info()[0]
            print(f"error: {e}")
            return render_template("error.html", error_message="Failed to search")
    else:
        return render_template("error.html", error_massage="You have to sign in first")
