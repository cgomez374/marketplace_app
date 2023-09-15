from main import app, display_msg_and_redirect
from flask import render_template, request, jsonify
from models import Product
import stripe
import json
import locale


# STRIPE
stripe.api_key = '#'
STRIPE_PK = '#'
GOOGLE_MAPS_KEY = '#'


@app.route('/', methods=['GET'])
def main():
    # db.drop_all()
    # db.create_all()
    products = Product.query.all()
    categories = []
    for product in products:
        if product.category not in categories:
            categories.append(product.category)
    return render_template('main.html', products=products, categories=categories, locale=locale)


@app.route('/product/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return display_msg_and_redirect('Product not found', 'main')
    return render_template('product_detail.html', product=product, locale=locale)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_data = request.json
        products = [[value['name'], value['price']] for key, value in product_data.items()]
        return jsonify({'message': 'Request processed successfully'}), 200
    return render_template('cart.html', locale=locale)


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
