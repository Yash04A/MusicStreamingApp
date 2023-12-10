from flask import Blueprint, render_template, request, url_for, flash,redirect, abort
from flask_login import login_required, current_user

from config import app, db
from models import Albums, Songs, User
from utils import uploadData
from forms import AlbumForm


album_bp = Blueprint('album',__name__)

@album_bp.before_request
@login_required
def check_user_role():
    check_rp = ['album.album_detail']
    if request.endpoint not in check_rp:
        if current_user.role not in ("admin", "creator"):
            app.logger.info(f"Access denied: {current_user.id} - {current_user.username} - {current_user.role}")
            abort(403)

@album_bp.route('/album/<int:album_id>')
def album_detail(album_id):
    album, username = db.session.query(Albums, User.username).join(User).filter(Albums.album_id==album_id).first()
    return render_template("albums/album_detail.html", album=album, username=username, pagetilte='album')
    
@album_bp.route('/album/update/<int:album_id>', methods=["GET","POST"])
@album_bp.route('/album/create', methods=["GET","POST"])
def create_album(album_id=None):
    form = AlbumForm()
    songs = db.session.query(Songs.song_id, Songs.title, Songs.duration, Songs.img).filter(Songs.is_flagged.is_(False)).all()

    if form.validate_on_submit():
        title = form.title.data
        img_file = form.img.data
        released_date = form.released_date.data
        selected_songs = request.form.getlist('selected_songs')

        if album_id:
            album = Albums.query.get(album_id)
            album.title = title
            
        else:
            album = Albums(title=title, release_date=released_date, creator_id=current_user.id)
            db.session.add(album)
            db.session.commit()

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
        form.released_date.data = album.release_date
        selected_songs = [song.song_id for song in album.songs]
        return render_template("albums/edit_album.html", form=form, songs=songs, selected=selected_songs, btn='Update' )
        
    return render_template("albums/edit_album.html", form=form, songs=songs, btn='Create')

@album_bp.route('/album/delete/<int:album_id>')
def delete_album(album_id):
    album = Albums.query.get(album_id)
    if current_user.id == Albums.user_id or current_user.role=='admin':
        if album:
            app.logger.info(f"Deleted Album - {album.title, album.album_id} ")
            db.session.delete(album)
            db.session.commit()

        else:
            app.logger.info(f"Album not found: {album_id}")
            flash('Album not found!')
    else:
        abort(403)
    return redirect(url_for('home'))




    


