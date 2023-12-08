from flask import Blueprint, render_template, request, url_for, flash,redirect, abort, current_app
from flask_login import login_required, current_user

from config import app, db
from models import Albums, Songs
from utils import uploadData
from forms import AlbumForm


album_bp = Blueprint('album',__name__)

@album_bp.before_request
@login_required
def check_user_role():
    check_rp = ['album.album_detail']
    if request.endpoint not in check_rp:
        if current_user.role not in ("admin", "creator"):
            abort(403)

@album_bp.route('/album/<int:album_id>')
def album_detail(album_id):
    album = Albums.query.filter_by(album_id=album_id).all()
    return "hello"
    
@album_bp.route('/album/update/<int:album_id>')
@album_bp.route('/album/create')
def create_album(album_id=None):
    form = AlbumForm()
    songs = db.session.query(Songs.song_id, Songs.title, Songs.duration, Songs.img).filter(Songs.creator_id == current_user.id).all()

    if form.validate_on_submit():
        title = form.title.data
        img_file = form.img.data
        release_date = form.release_date.data
        selected_songs = form.songs.data

        if album_id:
            album = Albums.query.get(album_id)
        else:
            album = Albums(title=title, release_date=release_date, user_id=current_user.id)
        
        if img_file:
            img_filename = f"{album.album_id}.jpg"
            img_path = uploadData(img_file, app.config['ALBUM_IMG_UPLOAD'], img_filename)
            album.img = img_path

        album.songs = Songs.query.filter(Songs.song_id.in_(selected_songs)).all()

        db.session.add(album)
        db.session.commit()

    if album_id:
        album = Albums.query.get(album_id)
        form.title.data = album.title
        form.release_date.data = album.release_date
        form.songs.choices = [(song.song_id, song.title) for song in album.songs]

        # album_songs = db.session.query(Songs.song_id).filter_by(album_id=album_id).all()
        # form.songs.choices = [(song.song_id, song.title) for song in album_songs]
    
    return render_template("edit_album.html", form=form, songs=songs)

@album_bp.route('/album/delete/<int:album_id>')
def delete_album(album_id):
    album = Albums.query.get(album_id)
    if current_user.id == Albums.user_id or current_user.role=='admin':
        if album:
            app.logger.info(f"Deleted Album - {album.title, album.album_id} ")
            db.session.delete(album)
            db.session.commit()
        else:
            flash('Song not found!')
    else:
        abort(403)
    return redirect(url_for('home'))




    


