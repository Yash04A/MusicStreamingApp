from flask import Flask, render_template, url_for, redirect, request, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from sqlalchemy.orm import session

from config import app,db
from forms import SongForm
from models import Songs, User, SongStats

from auth import auth_bp
from creator import creator_bp
from api.songs_api import song_bp
from api.playlist_api import playlist_bp
from api.album_api import album_bp


app.register_blueprint(auth_bp)
app.register_blueprint(song_bp, url_prefix='/songs')
app.register_blueprint(playlist_bp, url_prefix='/playlists')
app.register_blueprint(album_bp, url_prefix='/albums')
app.register_blueprint(creator_bp)


@app.route('/')
@app.route('/home')
@login_required
def home():
    r_songs = db.session.query(Songs.song_id, Songs.title, Songs.img, User.username).join(User).filter(Songs.is_flagged==0).order_by(func.random()).limit(6).all()
    new_songs = db.session.query(Songs.song_id, Songs.title, Songs.img, User.username).join(User).filter(Songs.is_flagged==0).order_by(Songs.song_id.desc()).limit(6).all()
    trending = db.session.query(Songs.song_id, Songs.title, Songs.img, User.username).join(User, User.id==Songs.creator_id).join(SongStats, SongStats.song_id==Songs.song_id).filter(Songs.is_flagged==0).order_by(SongStats.play_count.desc()).limit(6).all()
    print(trending)
    return render_template("home.html", r_songs=r_songs, new_songs=new_songs, trending=trending)


@app.route('/radio')
@login_required
def radio():
    pass


@app.route('/playlists')
@login_required
def playlists():
    pass


@app.route('/albums')
@login_required
def albums():
    pass



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
