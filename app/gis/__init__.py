from flask import Blueprint

gis = Blueprint('gis', __name__)

from . import views
