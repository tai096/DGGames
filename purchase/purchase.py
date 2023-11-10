from flask import Blueprint, redirect, render_template, request, session, flash
from models import Games, Orders, User, Purchases
from datetime import datetime
from app import db
from utils.tools import MessageType
from datetime import datetime

purchase_blueprint = Blueprint('purchase', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

@purchase_blueprint.route('/', methods=['POST', 'GET'])
def index():
    if 'current_user' in session:
        curr_user = session['current_user']

        purchases = Purchases.query.filter_by(customer_id = curr_user['id']).order_by(Purchases.date_of_purchase.desc()).all()

        purchased_games = []

        for purchase in purchases:
            purchased_game = Games.query.filter_by(id = purchase.game_id).first()
            purchased_game.date_of_purchase = purchase.date_of_purchase.strftime("%m/%d/%Y, %H:%M")

            purchased_games.append(purchased_game)

        return render_template('my-purchases.html', purchased_games = purchased_games)
    else:
        return redirect('auth/login')



