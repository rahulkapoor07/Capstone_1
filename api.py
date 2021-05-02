# from flask import Flask, request, redirect, render_template, jsonify, flash, session,g
# from models import db, connect_db, User, Stock, Cryptocurrency, User_stock, User_cryptocurrency
# from flask_debugtoolbar import DebugToolbarExtension
# from forms import SignupForm, loginForm, TickerForm
# from calc import popular_ticker
# from sqlalchemy.exc import IntegrityError
# from werkzeug.datastructures import MultiDict
# import json
# from flask_wtf.csrf import CsrfProtect
# import sys

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stock_market.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)
# app.config['WTF_CSRF_CHECK_DEFAULT'] = False

# connect_db(app)
# db.create_all()



# app = Flask(__name__)
# csrf = CSRFProtect(app)
# csrf.init_app(app)

# @app.route('/api/stocks-crypto/post', methods=["POST"])
# def post_data():
#     response = request.json
#     data = MultiDict(mapping=response)
#     form = TickerForm(data, meta={'csrf': False})
#     if form.submit():
#         if response["type"] == "crypto":
#             stock_name = form.name.data
#             stock_symbol = form.ticker.data
#             price = form.price.data
#             region = form.region.data
#             if Stock.query.filter_by(ticker_symbol=stock_symbol).first():
#                 return "<h1>Already in database<h1/>"
#             else:
#                 stock = Stock(stock_name=stock_name, ticker_symbol=stock_symbol, stock_price=price)
#                 db.session.add(stock)
#                 db.session.commit()
#                 return "<h1>Added to database</h1>"
#         elif response["type"] == "equity":
#             crypto_name = form.name.data
#             crypto_symbol = form.ticker.data
#             price = form.price.data
#             region = form.region.data
#             if Cryptocurrency.query.filter_by(ticker_symbol=crypto_symbol).first():
#                 return "<h1>Already in database<h1/>"
#             else:
#                 crypto = Cryptocurrency(crypto_name=crypto_name, ticker_symbol=crypto_symbol, crypto_price=price)
#                 db.session.add(crypto)
#                 db.session.commit()
#                 return "<h1>Added to database</h1>"


