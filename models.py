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

    id = db.Column(db.Integer,autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


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

    id = db.Column(db.Integer, autoincrement=True)
    stock_name = db.Column(db.Text, primary_key=True)
    ticker_symbol = db.Column(db.Text, nullable=False, unique=True)
    stock_price = db.Column(db.Float,nullable=True)

class Cryptocurrency(db.Model):

    __tablename__="cryptocurrencies"

    id = db.Column(db.Integer, autoincrement=True)
    crypto_name = db.Column(db.Text, primary_key=True)
    ticker_symbol = db.Column(db.Text, nullable=False, unique=True)
    crypto_price = db.Column(db.Float,nullable=True)


class User_stock(db.Model):

    __tablename__="users_stocks"

    user_username = db.Column(db.Text, db.ForeignKey("users.username"), primary_key=True)
    stocks_stock_name = db.Column(db.Text, db.ForeignKey("stocks.stock_name"), primary_key=True)

class User_cryptocurrency(db.Model):

    __tablename__="users_cryptocurrencies"

    user_username = db.Column(db.Text, db.ForeignKey("users.username"), primary_key=True)
    cryptos_crypto_name = db.Column(db.Text, db.ForeignKey("cryptocurrencies.crypto_name"), primary_key=True)