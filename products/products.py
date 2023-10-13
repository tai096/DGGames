from flask import Blueprint, render_template

products_blueprint = Blueprint('products', __name__, template_folder='templates')

@products_blueprint.route('/')
def index():
    renderItem = render_template('components/Item.html', var = 'test var')
    renderSideBar = render_template('components/SideBar.html')
    renderDropdown = render_template('components/Dropdown.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown)

@products_blueprint.route('/<product_id>')
def product_detail(product_id):
    renderBreadcrumbs = render_template('components/Breadcrumbs.html', var = 'test var')

    return render_template('product-detail.html', Breadcrumbs = renderBreadcrumbs)