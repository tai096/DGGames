from flask import Blueprint, render_template, request

products_blueprint = Blueprint('products', __name__, template_folder='templates')

@products_blueprint.route('/')
def index():
    from models import Games, Platform, Genre

    # fetch games from db
    games_query = Games.query.order_by(Games.name.asc()).all()
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    renderItem = render_template('components/Item.html', games_query = games_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch)

@products_blueprint.route('/filter?platform=<platform>')
def filterByPlatform(platform):
    from models import Platform, Genre

    # fetch games from db
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()
    platform_query = Platform.query.filter_by(platform_name = platform).first()

    games_query = platform_query.games_on_platform


    renderItem = render_template('components/Item.html', games_query = games_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch)

@products_blueprint.route('/filter?genre=<genre>')
def filterByGenre(genre):
    from models import Platform, Genre

    # fetch games from db
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    genre_query = Genre.query.filter_by(genre_name = genre).first()
    games_query = genre_query.games_of_genre

    renderItem = render_template('components/Item.html', games_query = games_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch)

@products_blueprint.route('/<product_id>')
def product_detail(product_id):
    from models import Games

    game_query = Games.query.filter_by(id = product_id).first()

    renderBreadcrumbs = render_template('components/Breadcrumbs.html', product_name = game_query.name)

    return render_template('product-detail.html', Breadcrumbs = renderBreadcrumbs, game_query = game_query, platforms_of_game = game_query.platforms_of_game, genres_of_game = game_query.genres_of_game)

@products_blueprint.route('/search', methods = ['POST'])
def handle_search():
    from models import Games
    from models import Games, Platform, Genre

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    # Get data search_text from request
    search_text = request.form['search_input']

    games_query = Games.query.filter(Games.name.like(f'%{search_text}%')).all()

    renderItem = render_template('components/Item.html', games_query = games_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch, search_text = search_text)