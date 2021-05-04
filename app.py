from flask import Flask, request, redirect, render_template, jsonify, flash, session,g
from models import db, connect_db, User, Stock, Cryptocurrency, User_stock, User_cryptocurrency
from flask_debugtoolbar import DebugToolbarExtension
from forms import SignupForm, LoginForm, TickerForm
from calc import popular_ticker, search_stock
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import MultiDict
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stock_market_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if "username" in session:
        g.user = User.query.get(session["username"])

    else:
        g.user = None




@app.route('/')
def redirect_to_homepage():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def homepage():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authentication(username, password)
        if user:
            session['username'] = user.username
            flash(f'Welcome back! {user.username}', "success")
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Please enter valid username/password']
    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # new_user = User.register(first_name, last_name, username, email, password)
        if User.query.filter_by(username=username).first():
            db.session.rollback()
            flash('Username already taken! Please try different username', "error")
        else:
            new_user = User.register(first_name.capitalize(), last_name.capitalize(), username, email, password)
            if new_user:
                db.session.add(new_user)
                db.session.commit()
                session["username"] = new_user.username
                flash(f"Welcome {new_user.username}!", "success")
                return redirect(f'/users/{new_user.username}')
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    flash("You have been logged out successfully!", "success")
    return redirect('/')

#User profile============================
@app.route('/users/<username>')
def user_page(username):
    if not g.user:
        flash("Access unauthorized.", "error")
        return redirect("/")
    else:
        user = User.query.get(username)
        form = TickerForm()
        [stock, crypto] = popular_ticker()
        return render_template('userpage.html', user=user, stock=stock, crypto=crypto, form=form)

@app.route('/users/<username>/profile')
def user_profile(username):
    if not g.user:
        flash("Access unauthorized.", "error")
        return redirect("/")
    user = User.query.get(username)
    stocks = user.stocks;
    cryptos = user.cryptos;
    return render_template('user-profile.html', user=user, stocks=stocks, cryptos=cryptos)

@app.route('/users/<username>/profile/<int:stock_id>')
def stock_details(username, stock_id):
    user = User.query.get(username)
    stock = Stock.query.get_or_404(stock_id)
    crypto = Cryptocurrency.query.get_or_404(stock_id)
    return render_template('users-stock.html', stock=stock, crypto=crypto)

@app.route('/market/stock-crypto/search', methods=['GET', 'POST'])
def stock_crypto():
    form = TickerForm()
    user = g.user
    if form.validate_on_submit():
        symbol = form.ticker.data
        region = form.region.data
        data = search_stock(symbol, region)
        if data["type"] == "stock":
            if Stock.query.filter_by(ticker_symbol=symbol).first():
                stock = Stock.query.filter_by(ticker_symbol=symbol).first()
                return render_template('stock-profile.html', data=data, user=user, stock=stock)
            else:
                stock = Stock(stock_name=data["name"], ticker_symbol=data["symbol"],region=region, stock_price=data["price"])
                db.session.add(stock)
                db.session.commit()
                return render_template('stock-profile.html', data=data, user=user, stock=stock)
        elif data["type"] == "crypto":
            if Cryptocurrency.query.filter_by(ticker_symbol=symbol).first():
                crypto = Cryptocurrency.query.filter_by(ticker_symbol=symbol).first()
                return render_template('stock-profile.html', data=data, user=user, crypto=crypto)
            else:
                crypto = Cryptocurrency(crypto_name=data["name"], ticker_symbol=data["symbol"],region=region, crypto_price=data["price"])
                db.session.add(crypto)
                db.session.commit()
                return render_template('stock-profile.html', data=data, user=user, crypto=crypto)
        elif data["type"] == "not found":
            flash("Please put correct ticker symbol!", "error")
            return redirect(f'/users/{user.username}')
    else:
        return redirect(f'/users/{user.username}')


# API to add stock/crypto into users profile++++++++++++++++
@app.route("/users/profile/add", methods=['POST'])
def add_stock():
    response = request.json
    market_data = response["marketData"]
    user = g.user
    if market_data["type"] == "stock":
        if User_stock.query.filter(User_stock.user_username==user.username, User_stock.stock_id==market_data["id"]).all():
            return jsonify({"message" : "stock already added in joint table"})
        else:
            user_stock_table = User_stock(user_username=user.username, stock_id=market_data["id"])
            db.session.add(user_stock_table)
            db.session.commit()
            return (jsonify({"message": "stock added to db in joint table"}), 201)
    elif market_data["type"] == "crypto":
        if User_cryptocurrency.query.filter(User_cryptocurrency.user_username==user.username, User_cryptocurrency.crypto_id==market_data["id"]).all():
            return jsonify({"message" : "crypto already added in joint table"})
        else:
            user_cryptocurrency_table = User_cryptocurrency(user_username=user.username, crypto_id=market_data["id"])
            db.session.add(user_cryptocurrency_table)
            db.session.commit()
            return (jsonify({"message": "crypto added to db in joint table"}), 201)
    else:
        return (jsonify({"message": "error"}), 201)


#API to delete/remove stock/crypto from users profile++++++++++
@app.route('/users/profile/delete/<type>/<int:stock_id>', methods=['DELETE'])
def delete_stock(type, stock_id):
    stock = Stock.query.get_or_404(stock_id)
    crypto = Cryptocurrency.query.get_or_404(stock_id)
    user = g.user
    if type == "stock":
        User_stock.query.filter(User_stock.user_username==user.username, User_stock.stock_id==stock.id).delete()
        db.session.commit()
        return jsonify({"message": "stock deleted"})
    elif type == "crypto":
        User_cryptocurrency.query.filter(User_cryptocurrency.user_username==user.username, User_cryptocurrency.crypto_id==crypto.id).delete()
        db.session.commit()
        return jsonify({"message": "crypto deleted"})



# @app.errorhandler(404)
# def page_not_found(e):
#     """404 NOT FOUND page."""

#     return render_template('404.html'), 404