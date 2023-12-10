from flask import Blueprint, render_template, url_for, redirect, abort
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)

from models import Songs, User, Playlists, Albums, Stats, SongStats
from config import db, app
from utils import plot_graph


@admin_bp.before_request
@login_required
def check_user_role():
    if current_user.role not in ("admin"):
        abort(403)


@admin_bp.route("/admin-dashboard")
def admin_dashboard():
    top_10 = db.session.query(Songs.title, SongStats.play_count).join(SongStats, SongStats.song_id==Songs.song_id).filter(Songs.is_flagged.is_(False)).order_by(SongStats.play_count.desc()).limit(10).all()
    
    if top_10:
        plot_graph(top_10, f'{current_user.id}.png')
        loc = f'dashboard/{current_user.id}.png'
    else:
        loc=None
    
    t_user, t_songs, t_playlist = db.session.query(Stats.total_users,Stats.total_songs,Stats.total_playlists).first()
    top_3 = db.session.query(Songs.song_id, Songs.title, Songs.img, Songs.genre, User.username, SongStats.play_count).join(User, User.id==Songs.creator_id).join(SongStats, SongStats.song_id==Songs.song_id).filter(Songs.is_flagged.is_(False)).order_by(SongStats.play_count.desc()).limit(3).all()
    return render_template("dashboard/admin_dashboard.html", dashboard=loc, t_user=t_user, t_songs=t_songs, t_playlist=t_playlist, top_3=top_3)


@admin_bp.route("/admin/list-users")
def list_users():
    
    users = User.query.all()
    return render_template("lists/user.html", users=users)


@admin_bp.route("/admin/list-songs")
def list_songs():
    
    songs = db.session.query(Songs, User.username).join(User).all()
    return render_template('lists/song.html', songs=songs)


@admin_bp.route("/admin/list-playlist")
def list_playlists():
    
    playlists = db.session.query(Playlists, User.username).join(User).all()
    return render_template('lists/playlist.html', playlists=playlists)


@admin_bp.route("/admin/list-albums")
def list_albums():

    albums = db.session.query(Albums, User.username).join(User).all()
    return render_template('lists/album.html', albums=albums)


@admin_bp.route("/admin/ban-user/<int:user_id>")
def ban_user(user_id):

    user = User.query.filter_by(id=user_id).first()
    if user:
        if not user.is_banned:
            user.is_banned = True
        else:
            user.is_banned = False
        app.logger.info(f"User Ban - {user.is_banned} - { user.id} ")
        db.session.commit()
    return redirect(url_for('admin.list_users'))


@admin_bp.route("/admin/flag_song/<int:song_id>")
def flag_song(song_id):
    song = Songs.query.filter_by(song_id=song_id).first()
    if song:
        if not song.is_flagged:
            song.is_flagged = True
        else:
            song.is_flagged = False
        app.logger.info(f"Song Flagged - {song.is_banned} - { song.id} ")
        db.session.commit()
    return redirect(url_for('admin.list_songs'))



