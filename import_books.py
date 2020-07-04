import os
import csv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

if not os.getenv("DATABASE_URL"):
  raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.String, primary_key=True)
  username = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.id

class Book(db.Model):
  __tablename__ = "books"
  id = db.Column(db.Integer, primary_key=True)
  isbn = db.Column(db.String, nullable=False)
  title = db.Column(db.String, nullable=False)
  author = db.Column(db.String, nullable=False)
  year = db.Column(db.String, nullable=False)

  def __repr__(self):
    return '<Book %r>' % self.id

def main():
  with open('books.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
  with app.app_context():
    # initialize 
    # db.create_all()
    # db.session.commit()
    main()
