from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import requests

load_dotenv() 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

client = MongoClient('localhost', 27017)

db = client.flask_db
users = db.users

# Home page
@app.route('/')
def index():
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username, 'password': password})
        if user:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})
        if user:
            return 'Username already exists. Please choose a different username.'
        else:
            users.insert_one({'username': username, 'password': password})
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = users.find_one({'_id': ObjectId(user_id)})

        available_cryptos = ["BTCUSDT", "ETHBTC", "LTCBTC", "BNBBTC", "NEOBTC", "QTUMETH", "EOSETH", "SNTETH", "BNTETH"]

        if request.method == 'POST':
            selected_cryptos = request.form.getlist('cryptos')
            # Update the user's preferences in the database
            users.update_one({'_id': ObjectId(user_id)}, {'$set': {'cryptos': selected_cryptos}})
        else:
            # Load the user's preferences if available
            selected_cryptos = user.get('cryptos', [])

        # Fetch live data for selected cryptocurrencies from the Binance API
        base_url = "https://api.binance.com/api/v3/ticker/price?symbol="
        currency_data = []
        for currency in selected_cryptos:
            response = requests.get(base_url + currency)
            data = response.json()
            currency_data.append({'currency': currency, 'price': float(data['price'])})
        
        return render_template('dashboard.html', selected_cryptos=selected_cryptos, currency_data=currency_data, available_cryptos=available_cryptos)

    else:
        return redirect(url_for('login'))

@app.route('/get_currency_data', methods=['GET'])
def get_currency_data():
    selected_cryptos = request.args.getlist('selected_cryptos[]')

    # Fetch live data for selected cryptocurrencies from the Binance API
    base_url = "https://api.binance.com/api/v3/ticker/price?symbol="
    currency_data = []
    for currency in selected_cryptos:
        response = requests.get(base_url + currency)
        data = response.json()
        currency_data.append({'currency': currency, 'price': float(data['price'])})

    return jsonify(currency_data)

@app.route('/save_cryptos', methods=['POST'])
def save_cryptos():
    if 'user_id' in session:
        user_id = session['user_id']
        data = request.get_json()
        selected_cryptos = data.get('selectedCryptos', [])
        
        # Update the user's preferences in the database
        users.update_one({'_id': ObjectId(user_id)}, {'$set': {'cryptos': selected_cryptos}})
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'User not authenticated.'}), 401



if __name__ == '__main__':
   app.run(debug = True)