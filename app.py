from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

client = MongoClient('localhost', 27017)

db = client.flask_db
users = db.users

# Home page
@app.route('/')
def index():
    return 'Welcome to the home page!'

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

# Dashboard page
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = users.find_one({'_id': ObjectId(user_id)})
        return f'Welcome, {user["username"]}! You are now logged in.'
    return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(debug = True)