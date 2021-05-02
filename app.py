from flask import Flask, request, redirect, render_template, jsonify, flash, session,g
from models import db, connect_db, User, Stock, Cryptocurrency, User_stock, User_cryptocurrency
from flask_debugtoolbar import DebugToolbarExtension
from forms import SignupForm, loginForm, TickerForm
from calc import popular_ticker
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
    form = loginForm()
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
            new_user = User.register(first_name, last_name, username, email, password)
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
    user = User.query.get(username)
    return render_template('user-profile.html', user=user)

@app.route('/api/stocks-crypto/post', methods=["POST"])
def post_data():
    response = request.json
    res_dict = response['params']
    data = MultiDict(mapping=res_dict)
    form = TickerForm(data, meta={'csrf': False})
    if form.validate():
        if res_dict["type"] == "equity":
            stock_name = form.name.data
            stock_symbol = form.ticker.data
            price = form.price.data
            region = form.region.data
            if Stock.query.filter_by(ticker_symbol=stock_symbol).first():
                db.session.rollback()
                return (jsonify({"error": "<h1>Stock already exists in database</h1>"}), 201)
            else:
                stock = Stock(stock_name=stock_name, ticker_symbol=stock_symbol, stock_price=price)
                db.session.add(stock)
                db.session.commit()
                return (jsonify({"result" : "<h1> Stock Added to database</h1>"}), 201)
        elif res_dict["type"] == "crypto":
            crypto_name = form.name.data
            crypto_symbol = form.ticker.data
            price = form.price.data
            region = form.region.data
            if Cryptocurrency.query.filter_by(ticker_symbol=crypto_symbol).first():
                db.session.rollback()
                return (jsonify({"error" : "<h1>Crypto Already in database<h1/>"}), 201)
            else:
                crypto = Cryptocurrency(crypto_name=crypto_name, ticker_symbol=crypto_symbol, crypto_price=price)
                db.session.add(crypto)
                db.session.commit()
                return (jsonify({"result" : "<h1>Crypto Added to database</h1>"}), 201)

@app.route('/api/stock-crypto/search')
def stock_crypto():
    # ticker = request.args["ticker"]
    # region = request.args["region"]
    # username = session["username"]
    return render_template('stock-profile.html')




# @app.after_request
# def add_header(req):
#     """Add non-caching headers on every request."""

#     req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     req.headers["Pragma"] = "no-cache"
#     req.headers["Expires"] = "0"
#     req.headers['Cache-Control'] = 'public, max-age=0'
#     return req


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404