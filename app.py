from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Create users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Create expenses table with proper schema
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)
    
    conn.commit()
    conn.close()
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "username" not in request.form or "password" not in request.form:
            return jsonify({"status": "error", "message": "Missing form data"}), 400
        
        username = request.form["username"]
        password = request.form["password"]
        
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session["user"] = username
            print(f"Login successful for {username}")  # Debugging
            return jsonify({"status": "success", "redirect": "/main-menu"})
        
        print("Invalid login attempt")  # Debugging
        return jsonify({"status": "error", "message": "Invalid username or password"})

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if "username" not in request.form or "password" not in request.form or "pin" not in request.form:
            return jsonify({"status": "error", "message": "Missing form data"}), 400

        username = request.form["username"]
        password = request.form["password"]
        pin = request.form["pin"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        # Check if username exists
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            return jsonify({"status": "error", "message": "Username already exists"}), 400  # Return error properly

        # Insert new user
        c.execute("INSERT INTO users (username, password, pin) VALUES (?, ?, ?)", (username, password, pin))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "redirect": "/login"})

    return render_template("register.html")



@app.route("/main-menu")
def main_menu():
    if "user" in session:
        return render_template("main-menu.html")
    return redirect(url_for("login"))

@app.route("/expense-tracker")
def expense_tracker():
    if "user" in session:  # Ensure the user is logged in
        return render_template("expense-tracker.html", username=session["user"])
    return redirect(url_for("login"))  # Redirect to login if not logged in

@app.route('/expenses', methods=['GET', 'POST', 'DELETE', 'PUT'])
def handle_expenses():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Not authenticated"}), 401

    username = session['user']
    
    if request.method == 'POST':
        data = request.get_json()
        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("""
                INSERT INTO expenses (username, amount, category, date)
                VALUES (?, ?, ?, ?)
            """, (username, data['amount'], data['category'], data['date']))
            conn.commit()
            return jsonify({"status": "success", "message": "Expense added"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        finally:
            conn.close()

    elif request.method == 'GET':
        # Handle filters
        time_filter = request.args.get('filter', 'month')
        start_date = request.args.get('start')
        end_date = request.args.get('end')
        
        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            
            query = "SELECT id, amount, category, date FROM expenses WHERE username = ?"
            params = [username]
            
            if time_filter == 'week':
                query += " AND date >= date('now', '-7 days')"
            elif time_filter == 'month':
                query += " AND date >= date('now', '-1 month')"
            elif time_filter == '3months':
                query += " AND date >= date('now', '-3 months')"
            elif time_filter == 'custom' and start_date and end_date:
                query += " AND date BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            c.execute(query, params)
            expenses = c.fetchall()
            return jsonify([{
                "id": row[0],
                "amount": row[1],
                "category": row[2],
                "date": row[3]
            } for row in expenses])
        finally:
            conn.close()

    elif request.method == 'DELETE':
        expense_id = request.args.get('id')
        if not expense_id:
            return jsonify({"status": "error", "message": "Missing expense ID"}), 400
        
        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("DELETE FROM expenses WHERE id = ? AND username = ?", 
                     (expense_id, username))
            conn.commit()
            return jsonify({"status": "success", "message": "Expense deleted"})
        finally:
            conn.close()

    elif request.method == 'PUT':
        data = request.get_json()
        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("""
                UPDATE expenses 
                SET amount = ?, category = ?, date = ?
                WHERE id = ? AND username = ?
            """, (data['amount'], data['category'], data['date'], 
                 data['id'], username))
            conn.commit()
            return jsonify({"status": "success", "message": "Expense updated"})
        finally:
            conn.close()



@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
