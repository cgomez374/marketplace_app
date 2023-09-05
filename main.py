from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import db, Merchant, Product
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret key'

# DB CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
db.init_app(app)

# Login Manager config
login_manager = LoginManager()
login_manager.init_app(app)


# User Loader
@login_manager.user_loader
def load_user(user_id):
    return Merchant.query.get(int(user_id))


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
    # db.drop_all()
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
            # Logs the merchant in
            login_user(merchant)
            return message_display_redirect('Successful login', 'account')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['merchant name'].strip()
        email = request.form['email'].strip()
        if Merchant.query.filter_by(email=email).first():
            return message_display_redirect('Email in use', 'signup')
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
        return message_display_redirect('Account Successfully created', 'login')
    return render_template('signup.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/merchant_account')
@login_required
def account():
    return render_template('merchant_account.html')


@app.route('/merchant_products', methods=['GET'])
@login_required
def view_products():
    merchant_products = Product.query.filter_by(merchant_id=current_user.id).all()
    return render_template('merchant_products.html', merchant_products=merchant_products)


# NEED TO IMPLEMENT FILE UPLOAD
@app.route('/new_product', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST':
        if request.form:
            print(request.form)
    return render_template('new_product.html')



