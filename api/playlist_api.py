from flask import Blueprint
from flask_restful import Api, Resource, reqparse

playlist_bp = Blueprint('playlist',__name__)
api = Api(playlist_bp)