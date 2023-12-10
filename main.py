from flask import Flask, render_template, url_for, redirect, request, abort, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, or_
import requests as rq

from config import app,db
from forms import SongForm
from models import Songs, User, SongStats, Like, Albums, Playlists

from auth import auth_bp
from creator import creator_bp
from admin import admin_bp
from api.songs_api import song_bp
from api.playlist_api import playlist_bp
from api.album_api import album_bp


@app.context_processor
def load_base():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return dict(user_playlists = db.session.query(Playlists.playlist_id, Playlists.title, Playlists.img).filter( Playlists.user_id==current_user.id).all())
    return dict()


app.register_blueprint(auth_bp)
app.register_blueprint(song_bp, url_prefix='/song')
app.register_blueprint(playlist_bp)
app.register_blueprint(album_bp)
app.register_blueprint(creator_bp)
app.register_blueprint(admin_bp)


@app.route('/')
@app.route('/home')
@login_required
def home():
    recommended = db.session.query(Songs.song_id, Songs.title, Songs.img, Songs.genre, User.username).join(User).filter(Songs.is_flagged.is_(False)).order_by(func.random()).limit(8).all()
    new_songs = db.session.query(Songs.song_id, Songs.title, Songs.img, Songs.genre, User.username).join(User).filter(Songs.is_flagged.is_(False)).order_by(Songs.release_date.desc()).limit(8).all()
    trending = db.session.query(Songs.song_id, Songs.title, Songs.img, Songs.genre, User.username).join(User, User.id==Songs.creator_id).join(SongStats, SongStats.song_id==Songs.song_id).filter(Songs.is_flagged.is_(False)).order_by(SongStats.play_count.desc()).limit(8).all()
    return render_template("home.html", recommended=recommended, new_songs=new_songs, trending=trending)


@app.route('/song/<string:title>-<int:song_id>')
@login_required
def played(title, song_id):
    response = rq.get(f"{url_for('song.songapi',song_id=song_id,_external=True)}")
    if response.status_code != 200:
        render_template('error.html')
    
    json_play = response.json()
    return render_template('songs/play.html', json_play=json_play)


@app.route('/radio')
@login_required
def radio():
    play = db.session.query(Songs.song_id,Songs.title).filter(Songs.is_flagged.is_(False)).order_by(func.random()).first()
    return redirect(url_for('played', title=play.title, song_id=play.song_id))
    

@app.route('/playlists')
@login_required
def playlists():
    playlists_list = db.session.query(Playlists, User.username).join(User).order_by(func.random()).limit(16).all()
    new = db.session.query(Playlists, User.username).join(User).order_by(Playlists.created_on.desc()).limit(8).all()
    return render_template('playlists/playlists.html', recommended_1=playlists_list[:8], recommended_2=playlists_list[8:], new=new)


@app.route('/albums')
@login_required
def albums():
    albums_list = db.session.query(Albums, User.username).join(User).order_by(func.random()).limit(16).all()
    new = db.session.query(Albums, User.username).join(User).order_by(Albums.release_date.desc()).limit(8).all()
    return render_template('albums/albums.html', recommended_1=albums_list[:8], recommended_2=albums_list[8:], new=new)



@app.route('/liked_songs')
@login_required
def user_liked_songs():
    liked_song = db.session.query(Songs).join(Like).filter(Like.user_id == current_user.id, Songs.is_flagged.is_(False)).all()
    print(liked_song)
    return render_template('songs/liked_songs.html', liked_song=liked_song)


@app.route('/liked/<int:song_id>')
@login_required
def liked_song(song_id):
    check_like = Like.query.filter_by(song_id=song_id, user_id=current_user.id).first()
    print(check_like)
    if check_like is None:
        liked = Like(song_id=song_id, user_id=current_user.id)
        db.session.add(liked)
        db.session.commit()
        action = 'like'
    else:
        db.session.delete(check_like)
        db.session.commit()
        action = 'unlike'

    return jsonify({'action':action, 'check_like':bool(check_like)})


@app.route('/search', methods=['POST'])
def search():
    search = request.form.get('search')
    songs = db.session.query(Songs, User.username).join(User).filter(Songs.is_flagged.is_(False), or_(Songs.title.ilike(f"%{search}%"),Songs.genre.ilike(f"%{search}%"))).limit(8).all()
    playlists = db.session.query(Playlists, User.username).join(User).filter(Playlists.title.ilike(f"%{search}%")).limit(8).all()
    albums = db.session.query(Albums, User.username).join(User).filter(Albums.title.ilike(f"%{search}%")).limit(8).all()
    
    return render_template('searched.html', songs=songs, playlists=playlists, albums=albums)




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
