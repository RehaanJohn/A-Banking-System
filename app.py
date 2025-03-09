from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
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
        if "username" not in request.form or "password" not in request.form:
            return jsonify({"status": "error", "message": "Missing form data"}), 400
        
        username = request.form["username"]
        password = request.form["password"]
        
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return jsonify({"status": "success", "redirect": "/login"})
        except sqlite3.IntegrityError:
            return jsonify({"status": "error", "message": "Username already exists"})
    return render_template("register.html")

@app.route("/main-menu")
def main_menu():
    if "user" in session:
        return render_template("main-menu.html")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
