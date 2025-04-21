from flask import Flask, redirect, render_template, request
import platform
import os
import psycopg2


app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
@app.route('/')
def hello():
    container_details = get_container_details()
    return render_template('index.html', container=container_details)

def get_container_details():
    details = {
        'ip_address': platform.node(),
        'hostname': platform.node(),
        'os': platform.system(),
        'architecture': platform.machine(),
        'Python Version': platform.python_version(),
        'System_Info': platform.system(),
        'platform': platform.platform()
    }
    print(details)
    return details


def get_db_connection():
    create_todos_table_if_not_exists()
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        # Add logging or other error handling
        return None
    return conn

def create_todos_table_if_not_exists():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY,'
                'description text)')
    conn.commit()
    conn.close()
    if not todos:
        return "No todos found."

def initialize_db():
    create_todos_table_if_not_exists()

@app.route('/todos')
@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        description = request.form['description']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO todos (description) VALUES (%s)',
                    (description,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/todos')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM todos')
    todo_list = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('todos.html', todos=todo_list)

@app.route('/remove_todo/<int:todo_id>')
def remove_todo(todo_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM todos WHERE id = %s', (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/todos')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY,'
                'description text)')
    conn.commit()
    conn.close()
if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0', port=8000)
 
