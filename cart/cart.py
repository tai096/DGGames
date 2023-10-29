from flask import Blueprint, redirect, render_template, request, session, flash
from models import Games, Orders, User
from datetime import datetime
from app import db
from utils.tools import MessageType

cart_blueprint = Blueprint('cart', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

@cart_blueprint.route('/')
def index():
    curr_user = User.query.filter_by(id=2).first()
    orders = Orders.query.filter_by(customer_id = curr_user.id).all()
    games_in_cart = []
    subtotal = 0
    discount = 0
    taxes = 0
    if orders:
        for order in orders:
            game = Games.query.filter_by(id=order.game_id).first()
            games_in_cart.append(game)
            subtotal += game.price
        taxes = subtotal * 5 / 100
    total = subtotal + taxes + discount
    return render_template('cart/cart.html', cart=games_in_cart, subtotal=subtotal, discount=discount, taxes=taxes, total=total)

@cart_blueprint.route('/add', methods=["POST"])
def cart_add():
    game_id = int(request.form['product_id'])
    curr_user = User.query.filter_by(id=2).first()
    orders = Orders.query.filter_by(customer_id=curr_user.id).all()
    if request.method == "POST":
        found = False
        for order in orders:
            if order.game_id == game_id:
                found = True
                flash(f'This game was already in your cart!', category=MessageType['ERROR'].value)
                break
        if not found:
            newOrder = Orders(
                date_of_order = datetime.now(),
                customer_id = curr_user.id,
                game_id = game_id
            )
            db.session.add(newOrder)
            db.session.commit()
            orders_update = Orders.query.filter_by(customer_id=curr_user.id).all()
            cart_length = len(orders_update)
            session['cart_length'] = cart_length
            flash(f'Added to cart successfully!', category=MessageType['SUCCESS'].value)    

    return redirect(request.referrer)

@cart_blueprint.route('/remove/<game_id>')
def cart_remove(game_id):
    curr_user = User.query.filter_by(id=2).first()
    orders = Orders.query.filter_by(customer_id=curr_user.id).all()
    for order in orders:
        if order.game_id == int(game_id):
            db.session.delete(order)
    db.session.commit()
    orders_update = Orders.query.filter_by(customer_id=curr_user.id).all()
    cart_length = len(orders_update)
    session['cart_length'] = cart_length
    return redirect(request.referrer)