from flask import Blueprint, render_template, request, redirect
from app import db
from sqlalchemy import update

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route('/auth/login')
def admin_login():

    return render_template('admin-login.html')

@admin_blueprint.route('/')
def management():
    from models import Games

    # fetch games from db
    games_query = Games.query.all()

    return render_template('management.html', games_query = games_query)

@admin_blueprint.route('edit-product/<product_id>', methods = ['GET', 'POST'])
def edit_product(product_id):
    from models import Games

    game_query = Games.query.filter_by(id = product_id).first()

    if request.method == 'POST':
        if game_query:
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image = request.form['image_url']

            updated_game = Games(
                name = name,
                description = description,
                price = price,
                image = image,
                purchase_number = 0,
                publisher_id = game_query.publisher_id)

            db.session.commit()
            # return redirect('/')
        
    return render_template('edit-product.html', game_query = game_query)