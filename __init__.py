from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhhh...'
app.config['PFP_UPLOADS'] = path.join(path.dirname(path.realpath(__file__)), 'static/pfp/')
app.config['SONG_IMG_UPLOAD'] = path.join(path.dirname(path.realpath(__file__)), 'static/song/')
app.config['SONG_UPLOAD'] = path.join(path.dirname(path.realpath(__file__)), 'static/song/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.sqlite3'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'