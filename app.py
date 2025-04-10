from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import locale
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict

locale.setlocale(locale.LC_TIME, '')

def format_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%A %d/%m/%Y")

def format_price(price):
    return f"${float(price):,.2f}"

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not 'user_id' in session:
            flash("Ingresa con tu usuario para ver esta página.")
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    return wrapper

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                session_date TEXT NOT NULL,
                session_price REAL NOT NULL,
                pending BOOLEAN NOT NULL default 1,
                FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

init_db()

ALLOW_DELETE = True

ALL_FILTER = 'all'
PENDING_FILTER = 'pending'
PAID_FILTER = 'paid'

FILTERS = [
    ("TODOS", ALL_FILTER),
    ("PENDIENTES", PENDING_FILTER),
    ("PAGADOS", PAID_FILTER)
]

ALLOWED_EMAILS = {'emidesouches@gmail.com', 'luimuntaner@gmail.com'}

app = Flask(__name__)
app.secret_key = 'lui-psi-app'
app.permanent_session_lifetime = timedelta(days=365)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email not in ALLOWED_EMAILS:
            flash("Este email no está autorizado para registrarse.")
            return redirect(url_for('register'))

        if email and password:
            hashed_password = generate_password_hash(password)
            try:
                with sqlite3.connect("database.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
                    conn.commit()
                flash("Cuenta creada con éxito. Ahora podés iniciar sesión.")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash("Este email ya está registrado.")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user[1], password):
                session.permanent = True
                session['user_id'] = user[0]
                session['user'] = email
                flash("Ingresó correctamente.")
                return redirect(url_for('index'))
            else:
                flash("Email o contraseña incorrecto.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for('login'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        security = request.form['security']

        if '-08-17' not in security:
            flash("La respuesta a la pregunta de seguridad es incorrecta.")
            return redirect(url_for('reset_password'))

        password_hashed = generate_password_hash(new_password)

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()

            if result:
                cursor.execute("UPDATE users SET password = ? WHERE email = ?", (password_hashed, email))
                conn.commit()
                flash("Contraseña actualizada correctamente.")
                return redirect(url_for('login'))
            else:
                flash("No existe una cuenta registrada con ese email.")
                return redirect(url_for('reset_password'))

    return render_template("reset_password.html")

@app.route('/')
@login_required
def index():
    show = request.args.get("show")

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        query = "SELECT persons.id, persons.name, sessions.id, sessions.session_date, sessions.session_price, sessions.pending \
                    FROM persons LEFT JOIN sessions ON persons.id = sessions.person_id"

        if show == PENDING_FILTER:
            query += " AND sessions.pending = 1"
        elif show == PAID_FILTER:
            query += " AND sessions.pending = 0"

        query += " ORDER BY persons.name, sessions.session_date"
        cursor.execute(query)
        data = cursor.fetchall()

    grouped_sessions = defaultdict(list)
    total = 0

    for person_id, name, session_id, date, price, pending in data:
        grouped_session_key = (person_id,name)
            
        if date and price:
            total += 1
            session_data = (session_id, format_date(date), format_price(price), pending)
            grouped_sessions[grouped_session_key].append(session_data)

    return render_template('index.html', grouped_sessions=grouped_sessions, filters=FILTERS, allow_delete=ALLOW_DELETE, show=show, total=total)

@app.route('/add_person', methods=['GET', 'POST'])
@login_required
def add_person():
    if request.method == 'POST':
        name = request.form.get('name')

        if name:
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT OR IGNORE INTO persons (name) VALUES (?)", (name,))
                conn.commit()

        return redirect(url_for('add_session'))

    return render_template('form_person.html')

@app.route('/add_session', methods=['GET', 'POST'])
@login_required
def add_session():
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        session_date = request.form.get('session_date')
        session_price = request.form.get('session_price')

        if person_id and session_date and session_price:
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO sessions (person_id, session_date, session_price) VALUES (?, ?, ?)",
                    (person_id, session_date, session_price)
                )
                conn.commit()

        return redirect(url_for('index'))

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM persons")
        persons = cursor.fetchall()

    return render_template('form_session.html', persons=persons)

@app.route('/remove/<int:id>')
@login_required
def remove_session(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = ?", (id,))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/remove_person/<int:person_id>', methods=['GET', 'POST'])
@login_required
def remove_person(person_id):
    if request.method == 'POST':
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE person_id = ?", (person_id,))    
            cursor.execute("DELETE FROM persons WHERE id = ?", (person_id,))
            conn.commit()

        return redirect(url_for('index'))

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        name = cursor.execute("SELECT name FROM persons WHERE id = ?", (person_id,)).fetchone()[0]  

    return render_template('delete_person.html', person_id=person_id, name=name)

@app.route('/toggle_pending/<int:id>')
@login_required
def toggle_pending(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        pending = cursor.execute("SELECT pending FROM sessions WHERE id = ?", (id,)).fetchone()[0]
        cursor.execute("UPDATE sessions SET pending = ? WHERE id = ?", (not pending,id))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/update_session/<int:person_id>/<int:id>', methods=['GET', 'POST'])
@login_required
def update_session(person_id, id):
    if request.method == 'POST':
        session_date = request.form.get('session_date')
        session_price = request.form.get('session_price')

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sessions SET session_date = ?, session_price = ? WHERE id = ?",
                (session_date, session_price, id))
            conn.commit()

        return redirect(url_for('index'))

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        name, date, price = cursor.execute(
            "SELECT persons.name,sessions.session_date,sessions.session_price \
                FROM persons INNER JOIN sessions ON sessions.person_id=persons.id WHERE persons.id = ?",
            (person_id,)).fetchone()
    
    return render_template('form_edit.html', id=id, person_id=person_id, date=date, price=price, name=name)

if __name__ == '__main__':
    app.run(debug=True)
