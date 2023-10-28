from flask import Blueprint, redirect, render_template, request, session, flash
from models import Games

cart_blueprint = Blueprint('cart', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

@cart_blueprint.route('/')
def index():
    cart = []
    subtotal = 0
    discount = 0
    taxes = 0
    if 'cart' in session:
        cart = session.get('cart', [])
        for product in cart:
            subtotal += product['price']
        taxes = subtotal * 5 / 100
    total = subtotal + taxes + discount
    return render_template('cart/cart.html', cart=cart, subtotal=subtotal, discount=discount, taxes=taxes, total=total)

@cart_blueprint.route('/add', methods=["POST"])
def cart_add():
    product_id = request.form['product_id']
    product = Games.query.filter_by(id=product_id).first()
    if request.method == "POST":
        product_dict = {
            "id": product_id,
            "name": product.name,
            "price": product.price,
            "image": product.image
        }
        cart = session.get("cart", [])
        found = False
        for item in cart:
            if item["id"] == product_id:
                found = True
                flash(f'This game was already in your cart!', category='Failure')
                break
        if not found:
            cart.append(product_dict)
            flash(f'Added to cart successfully!', category='Success')
        session["cart"] = cart
    return redirect(request.referrer)

@cart_blueprint.route('/remove?game_id=<game_id>')
def cart_remove(game_id):
    cart = session.get("cart", [])
    new_cart = []

    for game in cart:
        if game['id'] == game_id:
            continue
        new_cart.append(game)
    session['cart'] = new_cart
    return render_template("cart/cart.html")