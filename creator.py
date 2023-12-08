from flask import Blueprint, render_template, request, url_for, flash,redirect, abort
from flask_login import login_required, current_user
import requests as rq

creator_bp = Blueprint('creator', __name__)

from models import Songs
from config import db, app
from forms import SongForm

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
def creator_dashboard(_):
    song_data = db.session.query(Songs.title, Songs.likes, )