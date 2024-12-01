from datetime import datetime

import requests
from flask import Flask, render_template, redirect, url_for, request
from config import Config
from models import db
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

register_routes(app)

TELEGRAM_BOT_TOKEN = 'TOKEN'
TELEGRAM_CHAT_ID = 'CHATID'

@app.route('/dashboard')
def dashboard():
    module = 'dashboard'
    return render_template('dashboard/dashboard.html', module=module)

@app.route('/')
def index():
    response = requests.get('http://localhost:5000/dashboard/products/list')  # Assuming your Flask app is running locally
    products = response.json()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    response = requests.get(f'http://localhost:5000/dashboard/products/{product_id}')  # Fetch from your own API
    product = response.json()
    print(product)
    return render_template('product_detail.html', product=product)


@app.route('/checkout/<int:product_id>', methods=['GET', 'POST'])
def checkout(product_id):
    response = requests.get(f'http://localhost:5000/dashboard/products/{product_id}')
    product = response.json()
    print(product)
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        orderDate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        message = f"Order Details:\n=================================\nProduct: {product['name']}\nPrice: ${product['price']}\n=================================\nCustomer Information:\nName: {name}\nPhone Number: {phone_number}\nEmail: {email}\nAddress: {address}\nDate: {orderDate}\n================================="

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        telegram_data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message
        }

        requests.post(telegram_url, data=telegram_data)

        return redirect(url_for('index'))

    return render_template('checkout.html', product=product)


if __name__ == '__main__':
    app.run(debug=True)
