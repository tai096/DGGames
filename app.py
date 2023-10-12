from flask import Flask
from general.general import general_blueprint
from auth.auth import auth_blueprint
from products.products import products_blueprint
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dggames.db'
db = SQLAlchemy(app)

app.register_blueprint(general_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(products_blueprint, url_prefix='/products')

