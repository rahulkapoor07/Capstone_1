from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    stocks = db.relationship('Stock', secondary="users_stocks", backref="user")
    cryptos = db.relationship('Cryptocurrency', secondary="users_cryptocurrencies", backref="user")

    @classmethod
    def register(cls, first_name, last_name, username, email, password):

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authentication(cls, username, password):

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else: 
            return False

class Stock(db.Model):

    __tablename__="stocks"

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    stock_name = db.Column(db.Text, nullable=False, unique=True)
    ticker_symbol = db.Column(db.Text, nullable=False, unique=True)
    region = db.Column(db.Text, nullable=False, default="US")
    which_type = db.Column(db.Text, nullable=False)
    stock_price = db.Column(db.Float,nullable=False)


class Cryptocurrency(db.Model):

    __tablename__="cryptocurrencies"

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    crypto_name = db.Column(db.Text, nullable=False, unique=True)
    ticker_symbol = db.Column(db.Text, nullable=False, unique=True)
    region = db.Column(db.Text, nullable=False, default="US")
    which_type = db.Column(db.Text, nullable=False)
    crypto_price = db.Column(db.Float,nullable=False)


class User_stock(db.Model):

    __tablename__="users_stocks"

    user_username = db.Column(db.Text, db.ForeignKey("users.username"),primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), primary_key=True)

class User_cryptocurrency(db.Model):

    __tablename__="users_cryptocurrencies"

    user_username = db.Column(db.Text, db.ForeignKey("users.username"), primary_key=True)
    crypto_id = db.Column(db.Integer, db.ForeignKey("cryptocurrencies.id"), primary_key=True)