from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import locale
from datetime import datetime
locale.setlocale(locale.LC_TIME, '')

def format_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%A %d/%m/%Y")

def format_price(price):
    return f"${float(price):,.2f}"

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
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

@app.route('/')
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

    grouped_sessions = {}
    total = 0
    for person_id, name, session_id, date, price, pending in data:
        if name not in grouped_sessions:
            grouped_sessions[(person_id,name)] = []
        if date and price:
            total += 1
            grouped_sessions[(person_id,name)].append((session_id, format_date(date), format_price(price), pending))

    return render_template('index.html', grouped_sessions=grouped_sessions, filters=FILTERS, allow_delete=ALLOW_DELETE, show=show, total=total)

@app.route('/add_person', methods=['GET', 'POST'])
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
def remove_session(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/remove_person/<int:id>/<name>', methods=['GET', 'POST'])
def remove_person(id, name):
    if request.method == 'POST':
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE person_id = ?", (id,))    
            cursor.execute("DELETE FROM persons WHERE id = ?", (id,))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('delete_person.html', id=id, name=name)

@app.route('/toggle_pending/<int:id>')
def toggle_pending(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        pending = cursor.execute("SELECT pending FROM sessions WHERE id = ?", (id,)).fetchone()[0]
        cursor.execute("UPDATE sessions SET pending = ? WHERE id = ?", (not pending,id))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/update_session/<int:id>/<name>', methods=['GET', 'POST'])
def update_session(id, name):
    if request.method == 'POST':
        session_date = request.form.get('session_date')
        session_price = request.form.get('session_price')
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE sessions SET session_date = ?, session_price = ? WHERE id = ?", (session_date, session_price, id))
            conn.commit()
        return redirect(url_for('index'))
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        date, price = cursor.execute("SELECT session_date,session_price FROM sessions WHERE id = ?", (id,)).fetchone()
    return render_template('form_edit.html', id=id, date=date, price=price, name=name)

if __name__ == '__main__':
    app.run(debug=True)
