from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                session_date TEXT NOT NULL,
                session_price REAL NOT NULL
            )
        """)
        conn.commit()

init_db()

@app.route('/')
def index():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people")
        people = cursor.fetchall()
    return render_template('index.html', people=people)

@app.route('/add', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form.get('name')
        session_date = request.form.get('session_date')
        session_price = request.form.get('session_price')
        
        if name and session_date and session_price:
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO people (name, session_date, session_price) VALUES (?, ?, ?)", (name, session_date, session_price))
                conn.commit()
        return redirect(url_for('index'))
    return render_template('form.html')

@app.route('/remove/<int:id>')
def remove_person(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM people WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
