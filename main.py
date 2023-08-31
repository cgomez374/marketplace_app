from flask import Flask, render_template, url_for, request, redirect
from models import db, Merchant
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret key'

# DB CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
db.init_app(app)

products = [
    {
        'id': 1,
        'name': 'android phone',
        'price': 1000,
        'category': 'smartphone',
        'image_url': '../static/images/android.jpg'
    },
    {
        'id': 2,
        'name': 'iphone',
        'price': 1000,
        'category': 'smartphone',
        'image_url': '../static/images/iphone.jpg'
    },
    {
        'id': 3,
        'name': 'android phone',
        'price': 1000,
        'category': 'smartphone',
        'image_url': '../static/images/android.jpg'
    },
    {
        'id': 4,
        'name': 'iphone',
        'price': 1000,
        'category': 'smartphone',
        'image_url': '../static/images/iphone.jpg'
    },
    {
        'id': 5,
        'name': 'android phone',
        'price': 1000,
        'category': 'smartphone',
        'image_url': '../static/images/android.jpg'
    },
    {
        'id': 6,
        'name': 'iphone',
        'price': 1000,
        'category': 'smartphone',
        'image_url': '../static/images/iphone.jpg'
    },
    {
        'id': 7,
        'name': 'android phone',
        'price': 1000,
        'category': 'smartphone',
        'image_url': '../static/images/android.jpg'
    },
    {
        'id': 8,
        'name': 'iphone',
        'price': 1000,
        'category': 'smartphone',
        'image_url': '../static/images/iphone.jpg'
    }
]

# ROUTES


@app.route('/')
def main():
    db.create_all()
    return render_template('main.html', products=products)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['merchant name']
        email = request.form['email']
        new_password = request.form['password']
        date_joined = datetime.today().date()
        new_merchant = Merchant(name=name, email=email, date_joined=date_joined)
        new_merchant.set_password(new_password)
        try:
            db.session.add(new_merchant)
            db.session.commit()
        except:
            print('error committing')
        print('success')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')
