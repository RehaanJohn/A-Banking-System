from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from password_manager import BankSystem
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Initialize the banking system
bank_system = BankSystem()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == bank_system.master_account['username']:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if bank_system.master_account['password'] == hashed_password:
            session['username'] = username
            return jsonify({'status': 'success', 'message': 'Master login successful!', 'redirect': url_for('master_menu')})
    elif username in bank_system.password_manager:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if bank_system.password_manager[username]['password'] == hashed_password:
            session['username'] = username
            return jsonify({'status': 'success', 'message': 'Login successful!', 'redirect': url_for('main_menu')})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid password!'})
    else:
        return jsonify({'status': 'error', 'message': 'Username not found!'})

# Register route
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    pin = request.form['pin']

    if len(username) < 7:
        return jsonify({'status': 'error', 'message': 'Username must be longer than 7 characters!'})
    if len(password) < 7:
        return jsonify({'status': 'error', 'message': 'Password must be longer than 7 characters!'})
    if not (pin.isdigit() and len(pin) == 4):
        return jsonify({'status': 'error', 'message': 'PIN must be a 4-digit integer!'})

    if username in bank_system.password_manager:
        return jsonify({'status': 'error', 'message': 'Username already taken!'})

    bank_system.register_user(username, password, pin)
    return jsonify({'status': 'success', 'message': 'Account created successfully!', 'redirect': url_for('home')})

# Main menu route
@app.route('/main_menu')
def main_menu():
    if 'username' not in session:
        return redirect(url_for('home'))
    username = session['username']
    return render_template('main_menu.html', username=username)

# Master menu route
@app.route('/master_menu')
def master_menu():
    if 'username' not in session or session['username'] != bank_system.master_account['username']:
        return redirect(url_for('home'))
    return render_template('master_menu.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Deposit route
@app.route('/deposit', methods=['POST'])
def deposit():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized!'})
    username = session['username']
    amount = float(request.form['amount'])
    if amount <= 0 or amount > 50000:
        return jsonify({'status': 'error', 'message': 'Invalid deposit amount!'})
    bank_system.deposit(username, amount)
    return jsonify({'status': 'success', 'message': f'Deposited ${amount} successfully!'})

# Withdraw route
@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized!'})
    username = session['username']
    pin = request.form['pin']
    amount = float(request.form['amount'])
    if amount <= 0 or amount > bank_system.password_manager[username]['balance']:
        return jsonify({'status': 'error', 'message': 'Invalid withdrawal amount!'})
    if pin != bank_system.password_manager[username]['pin']:
        return jsonify({'status': 'error', 'message': 'Incorrect PIN!'})
    bank_system.withdraw(username, amount)
    return jsonify({'status': 'success', 'message': f'Withdrew ${amount} successfully!'})

# Check balance route
@app.route('/balance')
def balance():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized!'})
    username = session['username']
    balance = bank_system.password_manager[username]['balance']
    return jsonify({'status': 'success', 'balance': balance})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)