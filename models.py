from sqlalchemy.sql import func
from sqlalchemy import event
from flask_login import UserMixin

from config import login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(10), nullable=False)
    pfp  = db.Column(db.String(255), nullable=False, default='img/default_pfp.jpg')
    password = db.Column(db.String(), nullable=False)
    is_banned = db.Column(db.Boolean, default=False)

    created_songs = db.relationship('Songs', backref='created_songs', lazy=True)
    likes = db.relationship('Like', backref='user_likes', lazy=True, cascade='all, delete-orphan')
    playlists = db.relationship('Playlists', backref='user_playlists', lazy=True, cascade='all, delete-orphan')
    albums = db.relationship('Albums', backref='user_albums', lazy=True, cascade='all, delete-orphan')
    

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Songs(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.String(10), nullable=True)
    audio = db.Column(db.String(255), nullable=True)
    lyrics = db.Column(db.String(255), nullable=True)
    img = db.Column(db.String(255), nullable=True, default='img/default_song.jpg')
    is_flagged = db.Column(db.Boolean, default=False)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'), nullable=True)
    playlists = db.relationship('Playlists', secondary='playlist_song_association', back_populates='songs', lazy='dynamic')
    likes = db.relationship('Like', backref='Song_likes', lazy=True, cascade='all, delete-orphan')


class Playlists(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(255), nullable=False, default='img/default_playlist.jpg')
    created_on = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Songs', secondary='playlist_song_association', back_populates='playlists', lazy='dynamic')

class Albums(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(255), nullable=False, default='img/default_album.jpg')
    release_date = db.Column(db.Date, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Songs', backref='Album', lazy=True)


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_users = db.Column(db.Integer, nullable=False)
    total_songs = db.Column(db.Integer, nullable=False)
    total_playlists = db.Column(db.Integer, nullable=False)

class SongStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False, unique=True)
    play_count = db.Column(db.Integer, nullable=False, default=0)
    total_likes = db.Column(db.Integer, nullable=False, default=0)
    
    def update_total_likes(self):
        self.total_likes = Like.query.filter_by(song_id=self.song_id).count()
        db.session.commit()

class CreatorStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    total_albums = db.Column(db.Integer, nullable=False)


playlist_song_association = db.Table('playlist_song_association',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.playlist_id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.song_id'))
)

@event.listens_for(Songs, 'after_insert')
def create_songstat(mapper, connection, target):
    song_stat = SongStats(song_id=target.song_id)
    db.session.add(song_stat)
    db.session.commit()


@event.listens_for(Like, 'after_insert')
@event.listens_for(Like, 'after_delete')
def update_total_likes(mapper, connection, target):
    song_id = target.song_id
    song_stats = SongStats.query.filter_by(song_id=song_id).first()
    if song_stats is not None:
        song_stats.update_total_likes()


@event.listens_for(SongStats, 'after_insert')
@event.listens_for(SongStats, 'after_update')
@event.listens_for(SongStats, 'after_delete')
def update_total_likes_songstats(mapper, connection, target):
    target.update_total_likes()