from flask import Blueprint
from flask_resful import Api, Resource, reqparse

playlist_bp = Blueprint('song',__name__)
api = Api(playlist_bp)