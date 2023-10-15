from flask import Blueprint, render_template

products_blueprint = Blueprint('products', __name__, template_folder='templates')

@products_blueprint.route('/')
def index():
    from models import Games, Platform, Genre

    # fetch games from db
    games_query = Games.query.all()
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    renderItem = render_template('components/Item.html', games_query = games_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown)

@products_blueprint.route('/<product_id>')
def product_detail(product_id):
    from models import Games

    game_query = Games.query.filter_by(id = product_id).first()

    renderBreadcrumbs = render_template('components/Breadcrumbs.html', product_name = game_query.name)

    return render_template('product-detail.html', Breadcrumbs = renderBreadcrumbs, game_query = game_query)