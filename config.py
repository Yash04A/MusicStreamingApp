from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from os import path


app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhhh...'
app.config['PFP_UPLOADS'] = path.join(path.dirname(path.realpath(__file__)), 'static/pfp/')
app.config['PLAYLIST_IMG_UPLOAD'] = path.join(path.dirname(path.realpath(__file__)), 'static/playlist/')
app.config['ALBUM_IMG_UPLOAD'] = path.join(path.dirname(path.realpath(__file__)), 'static/album/')

app.config['SONG_IMG_UPLOAD'] = path.join(path.dirname(path.realpath(__file__)), 'static/song/')
app.config['SONG_UPLOAD'] = path.join(path.dirname(path.realpath(__file__)), 'static/song/')
app.config['SONG_LYRICS_UPLOAD'] = path.join(path.dirname(path.realpath(__file__)), 'static/song/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tunein.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'auth.login'


