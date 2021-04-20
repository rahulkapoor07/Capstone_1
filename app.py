from flask import Flask, request, redirect, render_template, jsonify, flash, session
from models import db, connect_db, User, Stock, Cryptocurrency, User_stock, User_cryptocurrency
from flask_debugtoolbar import DebugToolbarExtension
from forms import SignupForm, loginForm
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stock_market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

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
            flash(f'Welcome back! {user.username}')
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Please enter valid username/password']
    
    return render_template('homepage.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User.register(first_name, last_name, username, email, password)
        if User.query.filter_by(username=username).first():
            flash('Username already taken! Please try different username')
        else:
            new_user = User.register(first_name, last_name, username, email, password)
            if new_user:
                db.session.add(new_user)
                db.session.commit()
                session["username"] = new_user.username
                flash(f"Welcome {new_user.username}!")
                return redirect(f'/users/{new_user.username}')
    return render_template('signup.html', form=form)

@app.route('/users/<username>')
def user_page(username):
    if "username" not in session or username != session['username']:
        flash("Please login first!")
        return redirect('/')
    else:
        user = User.query.get(username)
        return render_template('userpage.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')