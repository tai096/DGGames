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


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(50), nullable=False, unique=True)
    # Many to Many Relationship
    ...

    def __repr__(self):
        return f'Platform {self.platform_name}'


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(1024), nullable=True, default='https://www.uri.edu/wordpress/wp-content/uploads/home/sites/7/500x333.png')
    purchase_number = db.Column(db.Integer, nullable=False, default=0)
    # Foreign Key
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False) 
    # One to Many Relationship
    ...
    # Many to Many Relationship
    ...

    def __repr__(self):
        return f'Game {self.name}'
    

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_order = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Order {self.id}'
    

class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_purchase = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Purchase {self.id}'