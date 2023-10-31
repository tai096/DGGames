from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from utils.tools import MessageType
from models import Games, Platform, User, Orders

general_blueprint = Blueprint('general', __name__, template_folder='templates', static_folder='static', static_url_path='/assets')

@general_blueprint.route('/', methods=["POST", "GET"])
def index():
    game_hero_section = Games.query.filter_by(name='Rocket League').first()
    games_best_seller = Games.query.order_by(Games.purchase_number).limit(10).all()
    games_by_price = Games.query.order_by(Games.price).all()
    games_recommended = []
    pc = Platform.query.filter_by(platform_name='PC').first()
    curr_user = User.query.filter_by(id=2).first()
    session['current_user'] = []
    cart_length = 0
    if curr_user:
        orders = Orders.query.filter_by(customer_id = curr_user.id).all()
        cart_length = len(orders)
        session['subtotal'] = 0
        session['cart'] = []
        for order in orders:
            game_order_obj = {
                'image': order.game.image,
                'name': order.game.name,
                'price': order.game.price
            }
            session['cart'].append(game_order_obj)
            session['subtotal'] += order.game.price
            
        user_obj = {
            'username': curr_user.username,
            'name': curr_user.name,
            'budget': curr_user.budget
        }
        session['current_user'] = user_obj

    session['cart_length'] = cart_length

    for game in games_by_price:
        if pc in game.platforms_of_game:
            games_recommended.append(game)
            
    return render_template('general/index.html', games_best_seller=games_best_seller, games_recommended=games_recommended, game_hero_section=game_hero_section)