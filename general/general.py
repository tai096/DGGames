from flask import Blueprint, render_template, redirect, url_for, request, session, flash

from models import Games, Platform

general_blueprint = Blueprint('general', __name__, template_folder='templates', static_folder='static', static_url_path='/assets')

@general_blueprint.route('/', methods=["POST", "GET"])
def index():
    game_hero_section = Games.query.filter_by(name='Rocket League').first()
    games_best_seller = Games.query.order_by(Games.purchase_number).limit(10).all()
    games_by_price = Games.query.order_by(Games.price).all()
    games_recommended = []
    pc = Platform.query.filter_by(platform_name='PC').first()
    for game in games_by_price:
        if pc in game.platforms_of_game:
            games_recommended.append(game)
    return render_template('general/index.html', games_best_seller=games_best_seller, games_recommended=games_recommended, game_hero_section=game_hero_section)

@general_blueprint.route('/cart/add', methods=["POST"])
def cart_add():
    try: 
        product_id = request.form['product_id']
        product = Games.query.filter_by(id=product_id).first()
        if request.method == "POST":
            message = []
            product_dict = {
                "id": product_id,
                "name": product.name,
                "price": product.price,
            }
            cart = session.get("cart", [])
            found = False
            for item in cart:
                if item["id"] == product_id:
                    found = True
                    message = (f'{item["name"]} was already in your cart!')
                    break
            if not found:
                cart.append(product_dict)
            session["cart"] = cart
            session["message"] = message
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)