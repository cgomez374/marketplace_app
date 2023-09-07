import botocore.exceptions
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import db, Merchant, Product
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import boto3

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

def message_display_redirect(message, redirect_to):
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


@app.route('/')
def main():
    # db.drop_all()
    # db.create_all()
    products = Product.query.all()
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
    return message_display_redirect('Logout successful', 'login')


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
        except SQLAlchemyError as e:
            db.session.rollback()
            message_display_redirect(e, 'signup')
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


@app.route('/new_product', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST' and request.form:
        product_name = request.form.get('product_name')
        product_price = request.form.get('product_price')
        product_category = request.form.get('product_category')
        product_img = request.files['product_img']
        image_url = ''

        current_products = Product.query.filter_by(merchant_id=int(current_user.id)).all()
        for product in current_products:
            if product.name == product_name:
                return message_display_redirect('Product name already exists', 'new_product')
        if product_img:
            image_url = upload_to_s3(product_img)
            # image_url = 'https://marketplace-product-images-bucket.s3.amazonaws.com/android.jpg'
        if not image_url:
            return message_display_redirect('File name must be unique', 'new_product')
        elif product_name and product_price and product_category:
            product_new = Product(name=product_name,
                                  price=product_price,
                                  category=product_category,
                                  img_url=image_url,
                                  merchant_id=int(current_user.id))
            try:
                db.session.add(product_new)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                print(str(e))
                return message_display_redirect('Error adding new product', 'view_products')
        return message_display_redirect('Successfully added new product!', 'view_products')
    return render_template('new_product.html')


@app.route('/product/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return message_display_redirect('Product not found', 'main')
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
        new_img_url = ''

        if new_image:
            new_img_url = upload_to_s3(file=new_image, update_object=True)
        if new_img_url:
            product_to_update.img_url = new_img_url
        product_to_update.name = new_name
        product_to_update.price = new_price
        product_to_update.category = new_category
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e))
            db.session.rollback()
            return message_display_redirect(str(e), 'update_product')
        return message_display_redirect('Update successful', 'view_products')
    return render_template('update_product.html', product=product_to_update)


@app.route('/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product_to_delete = Product.query.filter_by(id=product_id).first()
    if not product_to_delete:
        return message_display_redirect('Nothing to delete', 'view_products')
    match = product_to_delete.img_url.find('.com/') + 5
    result = delete_object_s3(product_to_delete.img_url[match:])
    if not result:
        return message_display_redirect('Error deleting image', 'view_products')
    db.session.delete(product_to_delete)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        return message_display_redirect('Error deleting product', 'view_products')
    return message_display_redirect('Delete successful', 'view_products')



