from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

def format_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

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
                FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

init_db()

@app.route('/')
def index():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT persons.id, persons.name, sessions.session_date, sessions.session_price
            FROM persons
            LEFT JOIN sessions ON persons.id = sessions.person_id
            ORDER BY persons.name, sessions.session_date
        """)
        data = cursor.fetchall()

    grouped_sessions = {}
    for person_id, name, date, price in data:
        if name not in grouped_sessions:
            grouped_sessions[name] = []
        if date and price:
            grouped_sessions[name].append((person_id, format_date(date), format_price(price)))

    return render_template('index.html', grouped_sessions=grouped_sessions)

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT OR IGNORE INTO persons (name) VALUES (?)", (name,))
                conn.commit()
        return redirect(url_for('index'))
    return render_template('form_person.html')

@app.route('/add_session', methods=['GET', 'POST'])
def add_session():
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        session_date = request.form.get('session_date')
        session_price = request.form.get('session_price')
        print(request.form.values())

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
        cursor.execute("DELETE FROM people WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
