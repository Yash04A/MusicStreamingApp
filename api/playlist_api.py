from flask import Blueprint, render_template, request, url_for, redirect, abort
from flask_login import login_required, current_user

from config import app, db
from models import Playlists, Songs, User
from utils import uploadData
from forms import PlaylistForm

playlist_bp = Blueprint('playlist',__name__)


@playlist_bp.before_request
@login_required
def check_user_role():
    pass

@playlist_bp.route('/playlist/<int:playlist_id>')
def playlist_detail(playlist_id):
    playlist, username = db.session.query(Playlists, User.username).join(User).filter(Playlists.playlist_id==playlist_id).first()
    return render_template("playlists/playlist_detail.html", playlist=playlist, username=username, pagetilte='Playlist')
    
@playlist_bp.route('/playlist/update/<int:playlist_id>', methods=["GET","POST"])
@playlist_bp.route('/playlist/create', methods=["GET","POST"])
def create_playlist(playlist_id=None):
    form = PlaylistForm()
    songs = db.session.query(Songs.song_id, Songs.title, Songs.duration, Songs.img).filter(Songs.is_flagged.is_(False)).all()

    if form.validate_on_submit():
        title = form.title.data
        img_file = form.img.data
        created_on = form.created_on.data
        selected_songs = request.form.getlist('selected_songs')

        if playlist_id:
            playlist = Playlists.query.get(playlist_id)
            playlist.title = title
            
        else:
            playlist = Playlists(title=title, created_on=created_on, user_id=current_user.id)
            db.session.add(playlist)
            db.session.commit()
        
        if img_file:
            img_filename = f"{playlist.playlist_id}.jpg"
            img_path = uploadData(img_file, app.config['PLAYLIST_IMG_UPLOAD'], img_filename)
            playlist.img = img_path

        playlist.songs = Songs.query.filter(Songs.song_id.in_(selected_songs)).all()

        db.session.add(playlist)
        db.session.commit()
        return redirect(url_for('playlist.playlist_detail', playlist_id=playlist.playlist_id))

    if playlist_id:
        playlist = Playlists.query.get(playlist_id)
        form.title.data = playlist.title
        form.created_on.data = playlist.created_on
        selected_songs = [song.song_id for song in playlist.songs]
        return render_template("playlists/edit_playlist.html", form=form, songs=songs, selected=selected_songs, btn='Update' )
        
    return render_template("playlists/edit_playlist.html", form=form, songs=songs, btn='Create')

@playlist_bp.route('/playlist/delete/<int:playlist_id>')
def delete_playlist(playlist_id):
    playlist = Playlists.query.get(playlist_id)
    if current_user.id == playlist.user_id or current_user.role=='admin':
        if playlist:
            app.logger.info(f"Deleted playlist - {playlist.title}{ playlist.playlist_id} ")
            db.session.delete(playlist)
            db.session.commit()
        else:
            app.logger.info(f"Playlist not found - {playlist_id} ")
    else:
        abort(403)
    return redirect(url_for('home'))




    


