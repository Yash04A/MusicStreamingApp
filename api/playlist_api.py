from flask import Blueprint, render_template, request, url_for, flash,redirect, abort, current_app
from flask_login import login_required, current_user

from config import app, db
from models import Playlists, Songs
from utils import uploadData
from forms import PlaylistForm

playlist_bp = Blueprint('playlist',__name__)


@playlist_bp.before_request
@login_required
def check_user_role():
    pass

@playlist_bp.route('/playlist/<int:playlist_id>')
def playlist_detail(playlist_id):
    playlist = Playlists.query.filter_by(playlist_id=playlist_id).all()
    return "hello"
    
@playlist_bp.route('/playlist/update/<int:playlist_id>')
@playlist_bp.route('/playlist/create')
def create_playlist(playlist_id=None):
    form = PlaylistForm()
    songs = db.session.query(Songs.song_id, Songs.title, Songs.duration, Songs.img).filter(Songs.is_flagged.is_(False)).all()

    if form.validate_on_submit():
        title = form.title.data
        img_file = form.img.data
        release_date = form.release_date.data
        selected_songs = form.songs.data

        if playlist_id:
            playlist = Playlists.query.get(playlist_id)
            
        else:
            playlist = Playlists(title=title, release_date=release_date, user_id=current_user.id)
        
        if img_file:
            img_filename = f"{playlist.playlist_id}.jpg"
            img_path = uploadData(img_file, app.config['PLAYLIST_IMG_UPLOAD'], img_filename)
            playlist.img = img_path

        playlist.songs = Songs.query.filter(Songs.song_id.in_(selected_songs)).all()

        db.session.add(playlist)
        db.session.commit()

    if playlist_id:
        playlist = Playlists.query.get(playlist_id)
        form.title.data = playlist.title
        form.release_date.data = playlist.release_date
        form.songs.choices = [(song.song_id, song.title) for song in playlist.songs]

        playlist_songs = db.session.query(Songs.song_id).filter_by(playlist_id=playlist_id).all()
        form.songs.choices = [(song.song_id, song.title) for song in playlist_songs]
    
    return render_template("edit_playlist.html", form=form, songs=songs)

@playlist_bp.route('/playlist/delete/<int:playlist_id>')
def delete_playlist(playlist_id):
    playlist = Playlists.query.get(playlist_id)
    if current_user.id == Playlists.user_id or current_user.role=='admin':
        if playlist:
            app.logger.info(f"Deleted playlist - {playlist.title, playlist.playlist_id} ")
            db.session.delete(playlist)
            db.session.commit()
        else:
            flash('Song not found!')
    else:
        abort(403)
    return redirect(url_for('home'))




    


