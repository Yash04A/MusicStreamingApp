from flask import Flask, render_template, url_for, redirect, request, abort
from flask_login import login_required, current_user

from config import app,db
from forms import SongForm

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
    return render_template("home.html")




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
