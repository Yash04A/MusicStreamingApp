from flask import Blueprint, request, flash, redirect, url_for
from flask_restful import Api, Resource
from flask_login import current_user
from mutagen.mp3 import MP3


from models import Songs, SongStats, User
from forms import SongForm
from config import db,app
from utils import uploadData


song_bp = Blueprint('song',__name__)
api = Api(song_bp)

class SongAPI(Resource):
    def get(self, song_id):
        try:
            song, username = db.session.query(Songs, User.username).join(User).filter(Songs.song_id==song_id).first()

            # read lyrics txt file
            loc = f'static/{song.lyrics}'
            with open(loc) as file:
                lyrics = file.read()

            if song :
                json_play = {
                    'song_id': song.song_id,
                    'title' : song.title,
                    'genre' : song.genre,
                    'release_date' : song.release_date.isoformat(),
                    'audio' : song.audio,
                    'lyrics' : lyrics,
                    'img' : song.img,
                    'artist': username
                }

                songstat= SongStats.query.filter_by(song_id=song_id).first()
                if songstat is not None:
                    songstat.play_count+=1
                    db.session.commit()
                else:
                    songstat = SongStats(song_id=song_id, play_count=1)
                    db.session.add(songstat)
                    db.session.commit()

                return json_play, 200
            else:
                return "Song not found", 404
            
        except Exception as e :
            app.logger.info(f"Error - {e} ")
            return 500

    def post(self):
        form = SongForm()

        if form.validate_on_submit():
            title = form.title.data
            genre = form.genre.data
            release_date = form.release_date.data
            audio_file = form.audio.data
            lyrics_file = form.lyrics.data
            img_file = form.img.data

            # get song duration
            audio = MP3(audio_file)
            duration_seconds = int(audio.info.length)
            duration_minutes = duration_seconds // 60
            duration_seconds %= 60
            duration = f"{duration_minutes:02d}:{duration_seconds:02d}"

            try:
                new_song = Songs(
                                title=title,
                                genre=genre,
                                release_date=release_date,
                                creator_id=current_user.id,
                                duration=duration
                )

                db.session.add(new_song)
                db.session.commit()

            except Exception as e :
                app.logger.info(f"Error - {e} ")
                flash("Error occured during initial commit!")
                return 500

            try:
                song_id = new_song.song_id

                # name files
                audio_filename = f"{song_id}.mp3"
                lyrics_filename = f"{song_id}.txt"
                img_filename = f"{song_id}.jpg"

                # Upload files
                audio_path = uploadData(audio_file, app.config['SONG_UPLOAD'], audio_filename)
                lyrics_path = uploadData(lyrics_file, app.config['SONG_LYRICS_UPLOAD'], lyrics_filename)
                img_path = uploadData(img_file, app.config['SONG_IMG_UPLOAD'], img_filename)

                # Update the Songs instance with file paths
                new_song.audio = audio_path
                new_song.lyrics = lyrics_path
                new_song.img = img_path

                stats = SongStats(
                    song_id=song_id,
                    play_count=0
                )
                db.session.add(stats)
                db.session.commit()
                
                app.logger.info(f"Song Added - {new_song.title} - { new_song.song_id}")
                flash("Song Uploaded Sucessfully!")
                return redirect(url_for('creator.upload_song'))
            
            except Exception as e :
                app.logger.info(f"Error - {e} ")
                return 500
        else:
            return redirect(url_for('creator.upload_song'))
        
    def put(self, song_id):
        form = request.get_json()
        title = form.get('title')
        genre = form.get('genre')

        try:
            update_song = Songs.query.filter_by(song_id=song_id).first()
            if update_song:
                if update_song.title != title:
                    update_song.title = title
                if update_song.genre != genre:
                    new_genre = genre
                    update_song.genre = new_genre
                db.session.commit()
                return "Song Updated Sucessfully", 200
            else:
                return "Song ",404
        except:
                return 500
        
        
    def delete(self, song_id):
        song = Songs.query.get(song_id)
        if song:
            db.session.delete(song)
            db.session.commit()
            return "Song deleted", 200
        
        else:
            return "No song found", 400
        
    
api.add_resource(SongAPI, '/','/<int:song_id>')