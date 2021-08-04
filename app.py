from flask import Flask, request, redirect, render_template, jsonify, flash, session,g
from models import db, connect_db, User, Stock, Cryptocurrency, User_stock, User_cryptocurrency
from flask_debugtoolbar import DebugToolbarExtension
from forms import SignupForm, LoginForm, TickerForm
from calc import popular_ticker, search_stock
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///stock_market_db')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///stock_market_db').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'SECRET!')
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


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
        [stocks, cryptos] = popular_ticker()
        return render_template('userpage.html', user=user, stocks=stocks, cryptos=cryptos, form=form)
            

@app.route('/users/<username>/profile')
def user_profile(username):
    if not g.user:
        flash("Access unauthorized.", "error")
        return redirect("/")
    user = User.query.get(username)
    stocks = user.stocks;
    cryptos = user.cryptos;
    return render_template('user-profile.html', user=user, stocks=stocks, cryptos=cryptos)

@app.route('/users/<username>/profile/<which_type>/<int:stock_id>')
def stock_details(username,which_type, stock_id):
    if not g.user:
        flash("Access unauthorized.", "error")
        return redirect("/")
    user = User.query.get(username)
    if which_type == "stock":
        stock = Stock.query.get_or_404(stock_id)
        stock_data = search_stock(stock.ticker_symbol, stock.region)
        flash("Please click refresh button to get latest price of stock!", "success")
        return render_template('users-stock.html',user=user, stock=stock, stock_data=stock_data)
    else:
        crypto = Cryptocurrency.query.get_or_404(stock_id)
        crypto_data = search_stock(crypto.ticker_symbol, crypto.region)
        flash("Please click refresh button to get latest price of cryptocurrency!", "success")
        return render_template('users-stock.html',user=user, crypto=crypto, crypto_data=crypto_data)

@app.route('/market/stock-crypto/search', methods=['GET', 'POST'])
def stock_crypto():
    if not g.user:
        flash("Access unauthorized.", "error")
        return redirect("/")
    form = TickerForm()
    user = g.user
    if form.validate_on_submit():
        symbol = form.ticker.data
        region = form.region.data
        data = search_stock(symbol, region)
        if data["type"] == "stock":
            if Stock.query.filter_by(ticker_symbol=symbol).first():
                stock = Stock.query.filter_by(ticker_symbol=symbol).first()
                return render_template('stock-profile.html', data=data, user=user,stock_data=data, stock=stock)
            else:
                stock = Stock(stock_name=data["name"], ticker_symbol=data["symbol"],region=region,which_type=data["type"], stock_price=data["price"])
                db.session.add(stock)
                db.session.commit()
                return render_template('stock-profile.html', data=data, user=user,stock_data=data, stock=stock)
        elif data["type"] == "crypto":
            if Cryptocurrency.query.filter_by(ticker_symbol=symbol).first():
                crypto = Cryptocurrency.query.filter_by(ticker_symbol=symbol).first()
                return render_template('stock-profile.html', data=data, user=user,crypto_data=data, crypto=crypto)
            else:
                crypto = Cryptocurrency(crypto_name=data["name"], ticker_symbol=data["symbol"],region=region,which_type=data["type"], crypto_price=data["price"])
                db.session.add(crypto)
                db.session.commit()
                return render_template('stock-profile.html', data=data, user=user,crypto_data=data, crypto=crypto)
        elif data["type"] == "not found":
            flash("Please insert correct ticker symbol for stocks and cryptocurrencies only!", "error")
            return redirect(f'/users/{user.username}')
    else:
        return redirect(f'/users/{user.username}')


# API to add stock/crypto into users profile++++++++++++++++
@app.route("/api/users/profile/add", methods=['POST'])
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
@app.route('/api/users/profile/delete', methods=['DELETE'])
def delete_stock():
    response = request.json
    user = g.user
    if response["type"] == "stock":
        remove_stock = User_stock.query.filter(User_stock.user_username==user.username, User_stock.stock_id==response["id"]).first()
        db.session.delete(remove_stock)
        db.session.commit()
        return jsonify({"message": "stock deleted"})
    elif response["type"] == "crypto":
        remove_crypto = User_cryptocurrency.query.filter(User_cryptocurrency.user_username==user.username, User_cryptocurrency.crypto_id==response["id"]).first()
        db.session.delete(remove_crypto)
        db.session.commit()
        return jsonify({"message": "crypto deleted"})

#API to change price in database+++++++++++++++++

@app.route('/api/stock-crypto/refresh', methods=['PATCH'])
def refreshPrice():
    response = request.json
    data = response["updateData"]
    market_data = search_stock(data["symbol"], data["region"])
    # user = User.query.get(data["username"])
    if data["type"] == "stock":
        stock = Stock.query.get_or_404(data["id"])
        stock.stock_price = market_data.get("price", stock.stock_price)
        db.session.add(stock)
        db.session.commit()

    if data["type"] == "crypto":
        crypto = Cryptocurrency.query.get_or_404(data["id"])
        crypto.crypto_price = market_data["price"]
        db.session.add(crypto)
        db.session.commit()
    return jsonify(msg="updated")