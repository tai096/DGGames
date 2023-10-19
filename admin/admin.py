from flask import Blueprint, render_template, request, redirect
from app import db
from sqlalchemy import update

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route('/auth/login')
def admin_login():

    return render_template('admin-login.html')

@admin_blueprint.route('/')
def management():
    from models import Games, Publisher, Genre, Platform

    # fetch games from db
    games_query = Games.query.all()
    publishers_query = Publisher.query.all()
    genres_query = Genre.query.all()
    platforms_query = Platform.query.all()

    render_modal_create_product = render_template('components/ModalCreateProduct.html', publishers_query = publishers_query, genres_query = genres_query, platforms_query = platforms_query)

    return render_template('management.html', games_query = games_query, ModalCreateProduct = render_modal_create_product)

@admin_blueprint.route('edit-product/<product_id>', methods = ['GET', 'POST'])
def edit_product(product_id):
    from models import Games, Publisher

    game_query = Games.query.filter_by(id = product_id).first()
    publishers_query = Publisher.query.all()

    if request.method == 'POST':
        if game_query:
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image = request.form['image_url']

            # Update the attributes of game_query
            game_query.name = name
            game_query.description = description
            game_query.price = price
            game_query.image = image

            db.session.commit()
        
    return render_template('edit-product.html', game_query = game_query, publishers_query = publishers_query, platforms_of_game = game_query.platforms_of_game, genres_of_game = game_query.genres_of_game, publisher = game_query.publisher)