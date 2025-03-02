from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from password_manager import BankSystem
import hashlib
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"Raw form data: {request.form}")  # Debug: Print raw form data
        print(f"Submitted username: {username}")  # Debug: Print username
        print(f"Submitted password: {password}")  # Debug: Print password

        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Username and password are required!'})

        # Master account login check
        if username == bank_system.master_account['username']:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if bank_system.master_account['password'] == hashed_password:
                session['username'] = username
                return jsonify({'status': 'success', 'message': 'Login successful!', 'redirect': url_for('master_menu')})
            return jsonify({'status': 'error', 'message': 'Invalid password!'})

        # Regular account login check
        if username in bank_system.password_manager:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if bank_system.password_manager[username]['password'] == hashed_password:
                session['username'] = username
                return jsonify({'status': 'success', 'message': 'Login successful!', 'redirect': url_for('main_menu')})
            return jsonify({'status': 'error', 'message': 'Invalid password!'})

        return jsonify({'status': 'error', 'message': 'Username not found!'})  # Username not found

    return render_template('index.html')  # Render the login page for GET requests

 

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        pin = request.form.get('pin')

        # Validation checks
        if len(username) < 7:
            return jsonify({'status': 'error', 'message': 'Username must be longer than 7 characters!'})
        if len(password) < 7:
            return jsonify({'status': 'error', 'message': 'Password must be longer than 7 characters!'})
        if not (pin.isdigit() and len(pin) == 4):
            return jsonify({'status': 'error', 'message': 'PIN must be a 4-digit integer!'})

        # Check if username already exists
        if username in bank_system.password_manager:
            return jsonify({'status': 'error', 'message': 'Username already taken!'})

        # Register the user
        bank_system.register_user(username, password, pin)
        # Debug: Print the password_manager dictionary after registration
        print("Current users in the system:", bank_system.password_manager)
        return jsonify({'status': 'success', 'message': 'Account created successfully!', 'redirect': url_for('home')})
    print("Raw form data:", request.form)
        

    # If GET request, render the registration page
    return render_template('register.html')


    

# Main menu route
@app.route('/main_menu')
def main_menu():
    if 'username' not in session:
        return redirect(url_for('home'))
    print(f"User {session['username']} accessed the main menu.")
    return render_template('main_menu.html', username=session['username'])

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