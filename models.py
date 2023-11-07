from flask_sqlalchemy import SQLAlchemy
from app import login_manager, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.string(10), nullable=False)
    pfp  = db.Column(db.String(25), nullable=False, default='default.jpg')
    password = db.Column(db.String(25), nullable=False)

class Song(db.Model):
    pass