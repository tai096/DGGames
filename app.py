from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dggames.db'
app.config['SECRET_KEY'] = '1fbd57e31d0ffb68ccbeb56c'
db = SQLAlchemy(app)

def format_currency(value):
    return "{:,.0f} VND".format(value).replace(',', '.')

from general.general import general_blueprint
from auth.auth import auth_blueprint
from products.products import products_blueprint
from admin.admin import admin_blueprint

app.register_blueprint(general_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(products_blueprint, url_prefix='/products')

app.jinja_env.filters['currency'] = format_currency

app.app_context().push()