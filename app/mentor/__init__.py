from flask import Blueprint

mentor = Blueprint('mentor', __name__)

from . import views