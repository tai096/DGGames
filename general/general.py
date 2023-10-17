from flask import Blueprint, render_template
from models import Genre, Games, Platform

general_blueprint = Blueprint('general', __name__, template_folder='templates',static_folder='static', static_url_path='/assets')

@general_blueprint.route('/')
def index():
    
    return render_template('general/index.html')