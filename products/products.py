from flask import Blueprint, render_template, request, flash
from utils.tools import MessageType

products_blueprint = Blueprint('products', __name__, template_folder='templates',  static_folder='static', static_url_path='/static')

@products_blueprint.route('/')
def index():
    from models import Games, Platform, Genre

    page = request.args.get('page', 1, type = int)

    # fetch games from db
    games_query = Games.query.paginate(page = page, per_page= 9)

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    renderItem = render_template('components/Item.html', games_query = games_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')
    renderPagination = render_template('components/Pagination.html', pages = games_query.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2), current_page = games_query.page)

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch, Pagination = renderPagination)

@products_blueprint.route('')
def filter_products():
    from models import Platform, Genre

    platform_text = request.args.get('platform', '', type = str)
    genre_text = request.args.get('genre', '', type = str)

    # fetch games from db
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    platform_query = Platform.query.filter_by(platform_name = platform_text).first()
    genre_query = Genre.query.filter_by(genre_name = genre_text).first()
    games_query = []
    if platform_query:
        games_query = platform_query.games_on_platform
    if genre_query:
        games_query = genre_query.games_of_genre
        

    renderItem = render_template('components/Item.html', games_query = games_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch)


@products_blueprint.route('/sort?=<sort_by>',)
def sort_products(sort_by):
    from models import Games, Platform, Genre

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()
    
    match sort_by:
        case "name_desc":
            games_query = Games.query.order_by(Games.name.desc()).all()
            option_value = "Name Z -> A"
        case "price_asc":
            games_query = Games.query.order_by(Games.price.asc()).all()
            option_value = "Price (low to high)"
        case "price_desc":
            games_query = Games.query.order_by(Games.price.desc()).all()
            option_value = "Price (high to low)"
        case _:
            games_query = Games.query.order_by(Games.name.asc()).all()
            option_value = "Name A -> Z"


    renderItem = render_template('components/Item.html', games_query = games_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html' , option_value = option_value)
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch)

@products_blueprint.route('/<product_id>')
def product_detail(product_id):
    from models import Games

    game_query = Games.query.filter_by(id = product_id).first()
    renderBreadcrumbs = render_template('components/Breadcrumbs.html', product_name = game_query.name)

    return render_template('product-detail.html', Breadcrumbs = renderBreadcrumbs, game_query = game_query, platforms_of_game = game_query.platforms_of_game, genres_of_game = game_query.genres_of_game, publisher = game_query.publisher, game_id=product_id)

@products_blueprint.route('', methods = ['POST'])
def handle_search():
    from models import Games
    from models import Games, Platform, Genre

    search_text = request.args.get('search', '', type = str)

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    games_query = Games.query.filter(Games.name.like(f'%{search_text}%')).all()

    renderItem = render_template('components/Item.html', games_query = games_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch, search_text = search_text)

@products_blueprint.route('/best-sellers')
def best_sellers():
    from models import Games, Platform, Genre

    pageTitle = 'BEST SELLERS'
    games_best_seller = Games.query.order_by(Games.purchase_number).limit(10).all()
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    renderItem = render_template('components/Item.html', games_query = games_best_seller)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch, pageTitle=pageTitle)

@products_blueprint.route('/featured-and-recommended')
def featured_recommended():
    from models import Games, Platform, Genre

    pageTitle = 'FEATURED AND RECOMMENDED'
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    games_by_price = Games.query.order_by(Games.price).all()
    games_recommended = []
    pc = Platform.query.filter_by(platform_name='PC').first()

    for game in games_by_price:
        if pc in game.platforms_of_game:
            games_recommended.append(game)

    renderItem = render_template('components/Item.html', games_query = games_recommended)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch, pageTitle=pageTitle)