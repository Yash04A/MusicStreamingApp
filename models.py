from flask_sqlalchemy import SQLAlchemy
from config import login_manager, db
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    pfp  = db.Column(db.String(25), nullable=False, default='default.jpg')
    password = db.Column(db.String(25), nullable=False)

# class Song(db.Model):
#     pass