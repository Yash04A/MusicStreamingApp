from flask import Blueprint
from flask_resful import Api, Resource, reqparse

song_bp = Blueprint('song',__name__)
api = Api(song_bp)
class SongAPI(Resource):
    def get(self, song_id):
        song = Songs.session.filterby(song_id=song_id)
        return song

    def post(self):
        pass

api.add_resource(SongAPI, '/')