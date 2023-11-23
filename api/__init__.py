from flask import Blueprint

song_bp = Blueprint('song', __name__)
playlist_bp = Blueprint('playlist', __name__)
album_bp = Blueprint('album', __name__)

from . import songs_api, playlist_api, album_api