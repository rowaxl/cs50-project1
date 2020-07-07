from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.String, primary_key=True)
  username = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.id

class Book(db.Model):
  __tablename__ = "books"
  isbn = db.Column(db.String, primary_key=True)
  title = db.Column(db.String, nullable=False)
  author = db.Column(db.String, nullable=False)
  year = db.Column(db.String, nullable=False)

  def __repr__(self):
    return '<Book %r>' % self.isbn

class Review(db.Model):
  __tablename__ = "reviews"
  id = db.Column(db.Integer, primary_key=True)
  book_isbn = db.Column(db.String, nullable=False)
  description = db.Column(db.String, nullable=False)
  user_name = db.Column(db.String, nullable=False)
  stars = db.Column(db.Integer, nullable=False)
  datetime = db.Column(db.Integer, nullable=False)
