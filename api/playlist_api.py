from flask import Blueprint
from flask_restful import Api, Resource, reqparse

playlist_bp = Blueprint('song',__name__)
api = Api(playlist_bp)