from flask import Blueprint
from flask_restful import Api, Resource, reqparse

album_bp = Blueprint('playlist',__name__)
api = Api(album_bp)