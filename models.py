from flask_sqlalchemy import SQLAlchemy
from config import login_manager, db
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(10), nullable=False)
    pfp  = db.Column(db.String(255), nullable=False, default='default.jpg')
    password = db.Column(db.String(), nullable=False)

    ratings = db.relationship('Rating', backref='user_ratings', lazy=True, cascade='all, delete-orphan')
    playlists = db.relationship('Playlists', backref='user_playlists', lazy=True, cascade='all, delete-orphan')
    albums = db.relationship('Albums', backref='user_albums', lazy=True, cascade='all, delete-orphan')



class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Songs(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    audio = db.Column(db.String(255), nullable=False)
    lyrics = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String(255), nullable=False)

    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'), nullable=False)
    playlists = db.relationship('Playlist', secondary='playlist_song_association', backref='songs', lazy='dynamic')
    ratings = db.relationship('Rating', backref='songs', lazy=True)


class Playlists(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Songs', secondary='playlist_song_association', backref='playlists', lazy='dynamic')

class Albums(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Songs', backref='album', lazy=True)


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_users = db.Column(db.Integer, nullable=False)
    total_songs = db.Column(db.Integer, nullable=False)
    total_playlists = db.Column(db.Integer, nullable=False)

class SongStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False, unique=True)
    play_count = db.Column(db.Integer, nullable=False)
    rating_average = db.Column(db.Float, nullable=False)

class CreatorStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    total_albums = db.Column(db.Integer, nullable=False)
    total_playlists = db.Column(db.Integer, nullable=False)


playlist_song_association = db.Table('playlist_song_association',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.playlist_id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.song_id'))
)