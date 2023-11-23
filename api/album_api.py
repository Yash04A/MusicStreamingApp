from flask import Blueprint
from flask_resful import Api, Resource, reqparse

album_bp = Blueprint('song',__name__)
api = Api(album_bp)