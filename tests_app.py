from unittest import TestCase
from app import app
from models import db, User, User_stock, Stock

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stock_market_db_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


db.drop_all()
db.create_all()

class AppTestCase(TestCase):

    def setUp(self):
        User.query.delete()
       
        user = User.register(first_name="Rahul", last_name="Kapoor", username="rahulkapoor", 
                email="rahulkapoor@gmail.com", password="rahulkapoor")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    # Testing homepage++++++++++++++++++++++++++++++
    def test_homepage(self):
        with app.test_client() as client:
            res = client.get("/")
            self.assertEqual(res.status_code, 302)
            self.assertIn(res.location, "http://localhost/login")

    def test_homepage_followed(self):
        with app.test_client() as client:
            res = client.get("/", follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<a class="navbar-brand" href="">Trade Screener</a>', html)
    

    # Testing login route+++++++++++++++++++++++++
    def test_login_page_with_correct_credentials(self):
        with app.test_client() as client:
            res = client.post("/login", data={"username": "rahulkapoor", "password": "rahulkapoor"}, 
                            follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="text-center text-light ml-5">Rahul Kapoor</h1>', html)
    
    def test_login_page_with_incorrect_credentials(self):
        with app.test_client() as client:
            res = client.post("/login", data={"username": "rahulkapoor", "password": "rahulkapoor123"}, 
                            follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn('<button type="submit" class="btn btn-primary btn-lg btn-block">Login</button>', html)
    

    # Testing signup route++++++++++++++++++++++++++++++++++++
    def test_signup_page_with_existing_username(self):
        with app.test_client() as client:
            res = client.post("/signup", data={'first_name':'Rahul', 'last_name' : 'Kapoor', 'username' : 'rahulkapoor', 
                'email' : 'rahulkapoor@gmail.com', 'password' : 'rahulkapoor', 'confirm': 'rahulkapoor'}, 
                            follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-primary btn-lg btn-block">Create Account</button>', html)

    def test_signup_page_with_unique_username(self):
        with app.test_client() as client:
            res = client.post("/signup", data={'first_name':'steve', 'last_name' : 'smith', 'username' : 'stevesmith', 
                'email' : 'stevesmith@gmail.com', 'password' : 'stevesmith', 'confirm':'stevesmith'},
                            follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="text-center text-light">Trending Stocks</h2>', html)
    


    # Logout route+++++++++++++++++++++++++
    def test_logout_route(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'rahulkapoor'
            res = client.get("/logout", follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-primary btn-lg btn-block">Login</button>', html)

    def test_user_page(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'rahulkapoor'
            res = client.get("/users/rahulkapoor")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="text-center text-light">Trending Stocks</h2>', html)


    def test_user_profile(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'rahulkapoor'
            res = client.get("/users/rahulkapoor/profile")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h4 class="text-light">Username: <b>rahulkapoor</b></h4>', html)





class StockCryptoTestCase(TestCase):
    def setUp(self):
        print("*********first***********")
        User_stock.query.delete()
        User.query.delete()
        Stock.query.delete()
       
        user = User.register(first_name="rahul", last_name="kapoor", username="rahulkapoor", 
                email="rahulkapoor@gmail.com", password="rahulkapoor")
        db.session.add(user)
        db.session.commit()

        stock = Stock(stock_name="Facebook, Inc.", ticker_symbol="fb",region="US", 
                    which_type="stock", stock_price="306.1696")
        db.session.add(stock)
        db.session.commit()
        self.stock_id = stock.id
        self.type = stock.which_type
        self.name = stock.stock_name
        self.region = stock.region
        self.symbol = stock.ticker_symbol
        self.price = stock.stock_price

    def tearDown(self):
        print("*******last************")
        
        db.session.rollback()

    def test_user_stock_profile(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'rahulkapoor'
            user_stock = User_stock(user_username="rahulkapoor", stock_id=self.stock_id)
            db.session.add(user_stock)
            db.session.commit()
            res = client.get(f"/users/rahulkapoor/profile/stock/{self.stock_id}")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<th scope="col">Ticker Symbol</th>', html)

    def test_search_stock(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'rahulkapoor'
            d = {"ticker" : "nio", "region" : "US"}
            res = client.post("/market/stock-crypto/search", data=d)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-primary btn-lg mt-3 py-2 follow-cls" id="follow-me-btn"><span>Follow</span></button>', html)
    

    def test_add_stock_crypto_api(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'rahulkapoor'
            d = {"marketData" : {"id": self.stock_id, "type" : self.type,"name": self.name, 
                "region" : self.region, "price": self.price}}
            res = client.post("/api/users/profile/add", json=d)
            self.assertEqual(res.status_code, 201)
            self.assertEqual(res.json, {"message": "stock added to db in joint table"})

    
    def test_delete_stock_crypto_api(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'rahulkapoor'
            user_stock = User_stock(user_username="rahulkapoor", stock_id=self.stock_id)
            db.session.add(user_stock)
            db.session.commit()
            d= {"id": self.stock_id, "type" : self.type,"name": self.name, 
                "region" : self.region, "price": self.price}
            res = client.delete("/api/users/profile/delete", json=d)
            print(res.json)
            self.assertEqual(res.json, {"message": "stock deleted"})

    
    def test_patch_stock_crypto_api(self):
        with app.test_client() as client:
            d = {"updateData" : {"id": self.stock_id, "type" : self.type,"name": self.name, 
                "region" : self.region,"symbol":self.symbol, "price": self.price}}
            res = client.patch("/api/stock-crypto/refresh", json=d)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json, {"msg": "updated"})