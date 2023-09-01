from flask import Flask, render_template, url_for, request, redirect, flash
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

def message_display_redirect(message, redirect_to):
    flash(message)
    return redirect(url_for(redirect_to))

@app.route('/')
def main():
    db.create_all()
    return render_template('main.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form:
            email_to_check = request.form.get('email')
            password_to_check = request.form.get('password')

            if not email_to_check or not password_to_check:
                message_display_redirect('Fields cannot be empty', 'login')

            merchant = Merchant.query.filter_by(email=email_to_check).first()
            if not merchant:
                message_display_redirect('Merchant not found', 'login')
            if not merchant.check_password(password_to_check):
                message_display_redirect('Email/password incorrect', 'login')
            flash('Successful login')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['merchant name'].strip()
        email = request.form['email'].strip()
        new_password = request.form['password'].strip()

        if not name or not email or not new_password:
            message_display_redirect('Fields cannot be empty', 'signup')

        date_joined = datetime.today().date()
        new_merchant = Merchant(name=name, email=email, date_joined=date_joined)
        new_merchant.set_password(new_password)
        try:
            db.session.add(new_merchant)
            db.session.commit()
        except:
            message_display_redirect('There was an error creating your account, please try again', 'signup')
        message_display_redirect('Account Successfully created', 'login')
    return render_template('signup.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')
