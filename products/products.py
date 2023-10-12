from flask import Blueprint, render_template

products_blueprint = Blueprint('products', __name__, template_folder='templates')

@products_blueprint.route('/')
def index():
    renderItem = render_template('components/Item.html')
    renderSideBar = render_template('components/SideBar.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar)