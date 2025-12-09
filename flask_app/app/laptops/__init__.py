from flask import Blueprint

laptops_bp = Blueprint('laptops', __name__, template_folder='templates')

from . import views