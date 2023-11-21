from flask import Blueprint, redirect, render_template, request, session, flash
from models import Games, Orders, User, Purchases
from app import db
from utils.tools import MessageType

purchase_blueprint = Blueprint('purchase', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

@purchase_blueprint.route('/', methods=['POST', 'GET'])
def index():
    if 'current_user' in session:
        curr_user = session['current_user']
        search_text = ''
        
        if request.method == "POST":
            search_text = request.form["search_input"]

            purchases = Purchases.query.filter_by(customer_id = curr_user['id']).join(Purchases.game).filter(Games.name.like(f'%{search_text}%')).order_by(Purchases.date_of_purchase.desc()).all()

        else:
            purchases = Purchases.query.filter_by(customer_id = curr_user['id']).order_by(Purchases.date_of_purchase.desc()).all()

        return render_template('my-purchases.html', purchases = purchases, search_text = search_text, method = request.method)
    else:
        return redirect('auth/login')



