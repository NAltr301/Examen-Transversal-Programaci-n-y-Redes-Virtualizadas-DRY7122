from flask import Flask, request
import sqlite3
import hashlib

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("usuarios.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT UNIQUE,
                        password_hash TEXT)""")
    conn.commit()
    conn.close()

def crear_usuario(nombre, password):
    hash_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("usuarios.db")
    conn.execute("INSERT OR REPLACE INTO usuarios (nombre, password_hash) VALUES (?,?)",
                 (nombre, hash_pw))
    conn.commit()
    conn.close()

def validar_usuario(nombre, password):
    hash_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("usuarios.db")
    cur = conn.execute("SELECT * FROM usuarios WHERE nombre=? AND password_hash=?",
                        (nombre, hash_pw))
    resultado = cur.fetchone()
    conn.close()
    return resultado is not None

@app.route("/")
def home():
    return "Servidor de autenticación activo (puerto 5800)"

@app.route("/login", methods=["POST"])
def login():
    nombre = request.form.get("nombre")
    password = request.form.get("password")
    if validar_usuario(nombre, password):
        return "Acceso concedido"
    return "Acceso denegado", 401

if __name__ == "__main__":
    init_db()
    # Carga inicial con los nombres de los integrantes
    crear_usuario("Nicolas Altamirano", "clave123")
    crear_usuario("Ignacio Andrade", "clave456")
    app.run(host="0.0.0.0", port=5800)