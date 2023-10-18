from flask import Blueprint, render_template
from models import Games, Platform

general_blueprint = Blueprint('general', __name__, template_folder='templates',static_folder='static', static_url_path='/assets')

@general_blueprint.route('/')
def index():
    games_best_seller = Games.query.order_by(Games.purchase_number).limit(10).all()
    games_by_price = Games.query.order_by(Games.price).all()
    games_recommended = []
    pc = Platform.query.filter_by(platform_name='PC').first()
    for game in games_by_price:
        if pc in game.platforms_of_game:
            games_recommended.append(game)
    return render_template('general/index.html', games_best_seller=games_best_seller, games_recommended=games_recommended)