from flask import Blueprint, render_template, request, redirect, flash
from utils.tools import MessageType
from app import db

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
    render_search = render_template('components/SearchBar.html')

    return render_template('management.html', games_query = games_query, ModalCreateProduct = render_modal_create_product, Search = render_search)

@admin_blueprint.route('/search', methods = ['POST'])
def handle_search():
    from models import Games, Publisher, Genre, Platform

    # fetch games from db
    publishers_query = Publisher.query.all()
    genres_query = Genre.query.all()
    platforms_query = Platform.query.all()

    search_text = request.form['search_input']
    games_query = Games.query.filter(Games.name.like(f'%{search_text}%')).all()

    render_modal_create_product = render_template('components/ModalCreateProduct.html', publishers_query = publishers_query, genres_query = genres_query, platforms_query = platforms_query)
    render_search = render_template('components/SearchBar.html')

    return render_template('management.html', games_query = games_query, ModalCreateProduct = render_modal_create_product, Search = render_search)

@admin_blueprint.route('create-product', methods = ['POST'])
def create_product():
    from models import Games, Genre, Platform

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image = request.form['image_url']
        purchase_number = 0
        publisher_id = request.form['publisher']
        genres = request.form.getlist('genres')
        platforms = request.form.getlist('platforms')

        new_game = Games(name = name, description = description, price = price, image = image,purchase_number = purchase_number ,publisher_id = publisher_id)
        new_game.genres_of_game = Genre.query.filter(Genre.id.in_(genres)).all()
        new_game.platforms_of_game = Platform.query.filter(Platform.id.in_(platforms)).all()

        try:
            db.session.add(new_game)
            db.session.commit()

            success_message = "Created successfully!"
            flash(f'{success_message}', category = MessageType['SUCCESS'].value)
        except:
            error_message = "Something went wrong! (POST: admin/create-product)"
            flash(f'Error: {error_message}', category = MessageType['ERROR'].value)

            db.session.rollback()
            
        finally:
            return redirect('/admin')

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
            publisher_id = request.form['publisher']

            # Update the attributes of game_query
            game_query.name = name
            game_query.description = description
            game_query.price = price
            game_query.image = image
            game_query.publisher_id = publisher_id

            try:
                db.session.commit()

                success_message = "Updated successfully!"
                flash(f'{success_message}', category = MessageType['SUCCESS'].value)
            except:
                error_message = "Something went wrong! (POST: admin/edit-product)"
                flash(f'Error: {error_message}', category = MessageType['ERROR'].value)

                db.session.rollback()

    return render_template('edit-product.html', game_query = game_query, publishers_query = publishers_query, platforms_of_game = game_query.platforms_of_game, genres_of_game = game_query.genres_of_game, publisher = game_query.publisher)

@admin_blueprint.route('delete-product/<product_id>', methods = ['POST'])
def delete_product(product_id):
    from models import Games

    game_query = Games.query.filter_by(id = product_id).first()

    if request.method == 'POST':
        if game_query:
            try:
                db.session.delete(game_query)  # Delete the product
                db.session.commit()  # Commit the changes

                success_message = "Deleted successfully!"
                flash(f'{success_message}', category = MessageType['SUCCESS'].value)

            except Exception as e:
                db.session.rollback()
                error_message = "Something went wrong! (POST: admin/delete-product)"
                flash(f'Error: {error_message}', category = MessageType['ERROR'].value)

            finally:
                return redirect('/admin')
