import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = 'clientes.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

@app.route('/add', methods=['POST'])
def add_cliente():
    nome = request.form.get('nome')
    email = request.form.get('email')

    if nome and email:
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO clientes (nome, email) VALUES (?, ?)', (nome, email))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            return "Erro: Este e-mail já está cadastrado.", 400
            
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)