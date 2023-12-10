from flask import Blueprint, render_template, url_for, flash,redirect, abort
from flask_login import login_required, current_user
import requests as rq

creator_bp = Blueprint('creator', __name__)

from models import Songs, Albums, SongStats, User
from config import db, app
from forms import SongForm
from utils import plot_graph

@creator_bp.before_request
@login_required
def check_user_role():
    if current_user.role not in ("admin", "creator"):
        abort(403)


@creator_bp.route("/upload/song")
def upload_song():

    return render_template("songs/upload_song.html", form=SongForm())

@creator_bp.route("/update/song/<int:song_id>", methods=['GET', 'POST'])
def update_song(song_id):
    song = Songs.query.get(song_id)
    form = SongForm(obj=song)
    if current_user.id == song.creator_id or current_user.role=='admin':
        if form.validate_on_submit():
            form_data = {
                'title': form.title.data,
                'genre': form.genre.data
            }
            response = rq.put(f"{url_for('song.songapi',song_id=song_id, _external=True)}",
                            json=form_data,
                            headers={'Content-Type':'application/json'})
            app.logger.info(f"Response: {response.status_code} - {response.text}")
            if response.status_code == 200:
                flash('Song Updated!')
            else:
                flash('Error in updating song.')
    else:
        abort(403)

    return render_template('songs/update_song.html', form=form, song=song)



@creator_bp.route("/delete/song/<int:song_id>")
def delete_song(song_id):
    song = Songs.query.get(song_id)

    if current_user.id == song.creator_id or current_user.role=='admin':
        response = rq.delete(f"{url_for('song.songapi',song_id=song_id,_external=True)}")
        app.logger.info(f"Response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            flash('Song deleted!')
        else:
            flash('Error deleting the song.')
    else:
        abort(403)

    return redirect(url_for('home'))

@creator_bp.route("/creator_dashboard/<string:username>")
def creator_dashboard(username):
    top_10 = db.session.query(Songs.title, SongStats.play_count).join(SongStats, SongStats.song_id==Songs.song_id).filter(Songs.is_flagged.is_(False), Songs.creator_id==current_user.id).order_by(SongStats.play_count.desc()).limit(10).all()
    
    if top_10:
        plot_graph(top_10, f'{current_user.id}.png')
        loc = f'dashboard/{current_user.id}.png'
    else:
        loc=None
    t_songs = Songs.query.filter_by(creator_id=current_user.id).count()
    t_albums = Albums.query.filter_by(creator_id=current_user.id).count()

    top_3 = db.session.query(Songs.song_id, Songs.title, Songs.img, Songs.genre, User.username, SongStats.play_count).join(User, User.id==Songs.creator_id).join(SongStats, SongStats.song_id==Songs.song_id).filter(Songs.is_flagged.is_(False), Songs.creator_id==current_user.id).order_by(SongStats.play_count.desc()).limit(3).all()
    return render_template("dashboard/creator_dashboard.html" ,dashboard=loc, t_songs=t_songs, t_albums=t_albums, top_3=top_3)


@creator_bp.route("/creator/albums")
def show_albums():
    albums = db.session.query(Albums, User.username).join(User).filter(Albums.creator_id==current_user.id).all()
    return render_template('lists/album.html', albums=albums)

@creator_bp.route("/creator/songs")
def show_songs():
    songs = db.session.query(Songs, User.username).join(User).filter(Songs.creator_id==current_user.id).all()
    return render_template('lists/song.html', songs=songs)