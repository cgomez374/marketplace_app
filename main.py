import botocore.exceptions
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import db, Merchant, Product
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import boto3
import stripe
import json

# STRIPE
stripe.api_key = '#'
STRIPE_PK = '#'
GOOGLE_MAPS_KEY = '#'

# AWS CREDENTIALS
AWS_ACCESS_KEY = '#'
AWS_SECRET_KEY = '#'

S3_CLIENT = boto3.client("s3",
                         aws_access_key_id=AWS_ACCESS_KEY,
                         aws_secret_access_key=AWS_SECRET_KEY)

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


# ROUTES

def display_msg_and_redirect(message, redirect_to):
    flash(message)
    return redirect(url_for(redirect_to))


# UPLOAD TO S3 BUCKET
def upload_to_s3(file, update_object=False):
    bucket_name = "marketplace-product-images-bucket"
    object_key = f'{current_user.name}/{file.filename}'
    if not update_object:
        try:
            response = S3_CLIENT.head_object(Bucket=bucket_name, Key=object_key)
            # If the object exists, handle the scenario as needed (e.g., show an error message)
            return None
        except Exception as e:
            # Upload the file to S3
            S3_CLIENT.upload_fileobj(file, bucket_name, object_key)
    elif update_object:
        S3_CLIENT.upload_fileobj(file, bucket_name, object_key)
    # Construct the URL of the uploaded file
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
    return s3_url


def delete_object_s3(object_key):
    bucket_name = "marketplace-product-images-bucket"
    try:
        S3_CLIENT.delete_object(Bucket=bucket_name, Key=object_key)
        return True
    except Exception as e:
        return False


@app.route('/', methods=['GET'])
def main():
    # db.drop_all()
    # db.create_all()
    products = Product.query.all()
    categories = []
    for product in products:
        if product.category not in categories:
            categories.append(product.category)
    return render_template('main.html', products=products, categories=categories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form:
            email_to_check = request.form.get('email').lower()
            password_to_check = request.form.get('password')

            if not email_to_check or not password_to_check:
                return display_msg_and_redirect('Fields cannot be empty', 'login')

            merchant = Merchant.query.filter_by(email=email_to_check).first()
            if not merchant:
                return display_msg_and_redirect('Merchant not found', 'login')
            if not merchant.check_password(password_to_check):
                return display_msg_and_redirect('Email/password incorrect', 'login')
            # Logs the merchant in
            login_user(merchant)
            return display_msg_and_redirect('Successful login', 'account')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return display_msg_and_redirect('Logout successful', 'login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['merchant name'].strip()
        email = request.form['email'].strip()
        if Merchant.query.filter_by(email=email.lower()).first():
            return display_msg_and_redirect('Email in use', 'signup')
        new_password = request.form['password'].strip()

        if not name or not email or not new_password:
            display_msg_and_redirect('Fields cannot be empty', 'signup')

        date_joined = datetime.today().date()
        new_merchant = Merchant(name=name, email=email.lower(), date_joined=date_joined)
        new_merchant.set_password(new_password)
        try:
            db.session.add(new_merchant)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            display_msg_and_redirect(e, 'signup')
        return display_msg_and_redirect('Account Successfully created', 'login')
    return render_template('signup.html')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_data = request.json
        products = [[value['name'], value['price']] for key, value in product_data.items()]
        return jsonify({'message': 'Request processed successfully'}), 200
    return render_template('cart.html')


@app.route('/checkout-success', methods=['GET'])
def checkout_success():
    return render_template('checkout_success.html')

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=data['items'][0]['total'] * 100,
            currency='usd',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/checkout', methods=['GET'])
def checkout():
    global STRIPE_PK
    global GOOGLE_MAPS_KEY
    return render_template('checkout.html', stripe_pk=STRIPE_PK, google_maps_key=GOOGLE_MAPS_KEY)


@app.route('/merchant_account')
@login_required
def account():
    return render_template('merchant_account.html')


@app.route('/merchant_update', methods=['GET', 'POST'])
@login_required
def merchant_update():
    if request.method == 'POST' and request.form:
        new_email = request.form.get('new_email')
        old_pass = request.form.get('old_password')
        new_pass = request.form.get('new_password')

        if not current_user.check_password(password_to_check=old_pass):
            return display_msg_and_redirect('Current password incorrect', 'merchant_update')
        if new_email:
            current_user.email = new_email
        if new_pass:
            current_user.set_password(new_password=new_pass)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return display_msg_and_redirect(str(e), 'merchant_update')
        return display_msg_and_redirect('Update successful', 'account')
    return render_template('merchant_update.html')


@app.route('/merchant_delete', methods=['GET'])
@login_required
def merchant_delete():
    db.session.delete(current_user)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return display_msg_and_redirect('Error deleting', 'account')
    return display_msg_and_redirect('Account deleted', 'signup')


@app.route('/merchant_products', methods=['GET'])
@login_required
def view_products():
    merchant_products = Product.query.filter_by(merchant_id=current_user.id).all()
    return render_template('merchant_products.html', merchant_products=merchant_products)


@app.route('/new_product', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST' and request.form:
        product_name = request.form.get('product_name')
        product_price = request.form.get('product_price')
        product_category = request.form.get('product_category')
        product_img = request.files['product_img']
        product_desc = request.form.get('product_description')
        image_url = ''

        current_products = Product.query.filter_by(merchant_id=int(current_user.id)).all()
        for product in current_products:
            if product.name == product_name:
                return display_msg_and_redirect('Product name already exists', 'new_product')
        if product_img:
            image_url = upload_to_s3(product_img)
            # image_url = 'https://marketplace-product-images-bucket.s3.amazonaws.com/android.jpg'
        if not image_url:
            return display_msg_and_redirect('File name must be unique', 'new_product')
        elif product_name and product_price and product_category and product_desc:
            product_new = Product(name=product_name,
                                  price=product_price,
                                  category=product_category,
                                  img_url=image_url,
                                  description=product_desc,
                                  merchant_id=int(current_user.id))
            try:
                db.session.add(product_new)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                print(str(e))
                return display_msg_and_redirect('Error adding new product', 'view_products')
        return display_msg_and_redirect('Successfully added new product!', 'view_products')
    return render_template('new_product.html')


@app.route('/product/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return display_msg_and_redirect('Product not found', 'main')
    return render_template('product_detail.html', product=product)


@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    product_to_update = Product.query.filter_by(id=product_id).first()
    if request.method == 'POST' and request.form:
        new_name = request.form.get('product_name')
        new_price = request.form.get('product_price')
        new_category = request.form.get('product_category')
        new_image = request.files['product_img']
        new_desc = request.form.get('product_description')
        new_img_url = ''

        if new_image:
            new_img_url = upload_to_s3(file=new_image, update_object=True)
        if new_img_url:
            product_to_update.img_url = new_img_url
        product_to_update.name = new_name
        product_to_update.price = new_price
        product_to_update.category = new_category
        product_to_update.description = new_desc
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e))
            db.session.rollback()
            return display_msg_and_redirect(str(e), 'update_product')
        return display_msg_and_redirect('Update successful', 'view_products')
    return render_template('update_product.html', product=product_to_update)


@app.route('/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product_to_delete = Product.query.filter_by(id=product_id).first()
    if not product_to_delete:
        return display_msg_and_redirect('Nothing to delete', 'view_products')
    match = product_to_delete.img_url.find('.com/') + 5
    result = delete_object_s3(product_to_delete.img_url[match:])
    if not result:
        return display_msg_and_redirect('Error deleting image', 'view_products')
    db.session.delete(product_to_delete)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        return display_msg_and_redirect('Error deleting product', 'view_products')
    return display_msg_and_redirect('Delete successful', 'view_products')




