from flask import Blueprint, request, flash, redirect, url_for
from flask_restful import Api, Resource, reqparse
from flask_login import current_user
from mutagen.mp3 import MP3
import os

from models import Songs, SongStats
from forms import SongForm
from config import db,app


song_bp = Blueprint('song',__name__)
api = Api(song_bp)

class SongAPI(Resource):
    def get(self, song_id):
        try:
            play = Songs.session.filterby(song_id=song_id)
            
            return play
        except :
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

            audio = MP3(audio_file)
            duration = audio.info.length

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
            except:
                flash("Error occured during initial commit!")
                return 500

            try:
                song_id = new_song.song_id

                audio_filename = f"{song_id}.mp3"
                lyrics_filename = f"{song_id}.txt"
                img_filename = f"{song_id}.jpg"

                # File paths
                audio_path = os.path.join(app.config['SONG_UPLOAD'], audio_filename)
                lyrics_path = os.path.join(app.config['LYRICS_UPLOAD'], lyrics_filename)
                img_path = os.path.join(app.config['IMG_UPLOAD'], img_filename)

                # Save file at given location
                audio_file.save(audio_path)
                lyrics_file.save(lyrics_path)
                img_file.save(img_path)

                # Update the Songs instance with file paths
                new_song.audio = audio_path
                new_song.lyrics = lyrics_path
                new_song.img = img_path

                db.session.commit()
                flash("Song Uploaded Sucessfully!")
                return redirect(url_for()), 201
            except:
                flash("Error occured!")
                return 500
        else:
            return {'error':form.errors}, 400
        
    def put(self, song_id):
        form = SongForm()

        if form.validate_on_submit():
            title = form.title.data
            genre = form.genre.data

            try:
                update_song = Songs.query.filter_by(song_id=song_id).first()
                if current_user.id == update_song.creator_id :
                    update_song.title = title
                    update_song.genre = genre
                    db.session.commit()

                    flash("Song Uploaded Sucessfully!")
                    return redirect(url_for()), 201
                else:
                    flash("Access denied!")
            except:
                flash("Error occured!")
                return 500
        else:
            return {'error':form.errors}, 400
        
    def delete(self, song_id):
        song = Songs.query.get(song_id)
        if song:
            if current_user.id == song.creator_id or current_user.role=='admin':
                song.delete()
                flash('Song deleted!')
            else:
                flash('Access denied!')
        else:
            flash("No song found!")
        return redirect('/')
    

api.add_resource(SongAPI, '/')