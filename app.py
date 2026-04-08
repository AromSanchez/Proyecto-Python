from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

DB_HOST = 'dpg-d71v6phr0fns738t5c10-a.oregon-postgres.render.com'
DB_NAME = 'test_xpec'
DB_USER = 'test_xpec_user'
DB_PASSWORD = 'iQyQwsfWRjaOQt4q6QKhF3RXWIAQOmkc'

def conectar_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            sslmode='require'  # <- obligatorio en Render
        )
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
            (dni, nombre, apellido, direccion, telefono)
        )
        conn.commit()
        conn.close()

def obtener_registros():
    conn = conectar_db()
    registros = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personas ORDER BY apellido")
        registros = cursor.fetchall()
        conn.close()
    return registros

def eliminar_por_dni(dni):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personas WHERE dni = %s", (dni,))
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    crear_persona(dni, nombre, apellido, direccion, telefono)
    return redirect(url_for('index'))

@app.route('/administrar')
def administrar():
    registros = obtener_registros()
    return render_template('administrar.html', registros=registros)

@app.route('/eliminar/<dni>', methods=['POST'])
def eliminar_registro(dni):
    eliminar_por_dni(dni)
    return redirect(url_for('administrar'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)