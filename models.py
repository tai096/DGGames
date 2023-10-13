#MODELS ARE TABLES IN DATABASE
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Enum('customer', 'admin'), nullable=False, default='customer')
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=True, unique=True)
    budget = db.Column(db.Integer, nullable=False, default=5000000)
    # One to Many Relationship (For customer)
    orders = db.relationship('Orders', backref='customer', lazy=True)
    purchases = db.relationship('Purchases', backref='customer', lazy=True)

    def __repr__(self):
        return f'User {self.username}'


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(30), nullable=False, unique=True)
    # One to Many Relationship
    games = db.relationship('Games', backref='genre', lazy=True)

    def __repr__(self):
        return f'Genre {self.genre_name}'


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(50), nullable=False, unique=True)
    # One to Many Relationship
    games = db.relationship('Games', backref='publisher', lazy=True)

    def __repr__(self):
        return f'Publisher {self.publisher_name}'

platform_games = db.Table('platform_games',
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'), primary_key=True),
    db.Column('games_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(50), nullable=False, unique=True)
    # Many to Many Relationship
    games_on_platform = db.relationship('Games', secondary=platform_games, lazy='subquery', backref=db.backref('platforms_of_game', lazy=True))

    def __repr__(self):
        return f'Platform {self.platform_name}'


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(1024), nullable=True, default='https://www.uri.edu/wordpress/wp-content/uploads/home/sites/7/500x333.png')
    purchase_number = db.Column(db.Integer, nullable=True, default=0)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False) 
    # One to Many Relationship
    order = db.relationship('Orders', backref='game', lazy=True)
    purchases = db.relationship('Purchases', backref='game', lazy=True)
    # Many to Many Relationship with: Platform (use 'platforms_of_game')

    def __repr__(self):
        return f'Game {self.name}'
    

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_order = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    # Many to One Relationship with: Customer (use 'customer'), Games (use 'game')

    def __repr__(self):
        return f'Order {self.id}'
    

class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_purchase = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    # Many to One Relationship with: Customer (use 'customer'), Games (use 'game')

    def __repr__(self):
        return f'Purchase {self.id}'