from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

# Import modules after defining the blueprint
from . import admin, error, main, reserve
