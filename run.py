import os
print("FILE:", os.path.abspath(__file__))
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from app.analyzer import analyze_password
from app.attacker import Attacker

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_in_production'
DB_NAME = 'users.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    analysis_result = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password:
            # Analyze password
            basic_analysis = analyze_password(password)
            
            # Simulate attacks
            attacker = Attacker()
            dict_attack = attacker.simulate_dictionary_attack(password)
            brute_force = attacker.estimate_brute_force(password)
            
            analysis_result = {
                "basic": basic_analysis,
                "dictionary": dict_attack,
                "brute_force": brute_force
            }
            
    return render_template('dashboard.html', result=analysis_result)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user_row = c.fetchone()
        conn.close()
        
        if user_row and check_password_hash(user_row[1], password):
            session['user_id'] = user_row[0]
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill out all fields', 'warning')
            return render_template('register.html')
            
        hashed_pw = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_pw))
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'danger')
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
