from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, FloatField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired("Please enter first name")], render_kw = {"placeholder" : "First Name"})
    last_name = StringField("Last Name", validators=[InputRequired("Please enter last name")], render_kw = {"placeholder" : "Last Name"})
    username = StringField("Username", validators=[InputRequired("Please enter username")], render_kw = {"placeholder" : "Username"})
    email = StringField("Email", validators=[InputRequired("Please enter email address"), Email("Please enter a valid email")], render_kw = {"placeholder" : "Email"})
    password = PasswordField('New Password', validators=[InputRequired("Please enter new password"), EqualTo('confirm', message='Passwords must match'), Length(min=4, max=20, message="Length of password should be between 8 to 16 characters")], render_kw = {"placeholder" : "Password"})
    confirm  = PasswordField('Repeat Password', render_kw = {"placeholder" : "Confirm Password"})

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[(InputRequired("Please enter username"))], render_kw = {"placeholder" : "Username"})
    password = PasswordField("password", validators= [InputRequired("Please enter password")], render_kw = {"placeholder" : "Password"})


class TickerForm(FlaskForm):
    ticker = StringField("Search Ticker",validators=[InputRequired("Please mention ticker symbol of stock")], render_kw = {"placeholder" : "Search Ticker"})
    REGION_CHOICES = [('US', 'US'), ('BR', 'BR'), ('AU', 'AU'),('CA', 'CA'), ('FR', 'FR'), ('DE', 'DE'), ('HK', 'HK'),
                    ('IN', 'IN'), ('IT', 'IT'), ('ES', 'ES'), ('GB', 'GB'), ('SG', 'SG')]
    region = SelectField('Region', choices=REGION_CHOICES, validators=[InputRequired()])
