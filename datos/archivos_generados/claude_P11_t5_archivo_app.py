import hashlib
import os
import secrets
import smtplib
import sqlite3
import sys
from datetime import datetime, timedelta
from email.message import EmailMessage

from flask import (Flask, flash, redirect, render_template_string, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

DB = "tienda.db"

app = Flask(__name__)
# Define SECRET_KEY como variable de entorno (una cadena larga y aleatoria)
app.secret_key = os.environ["SECRET_KEY"]

# Configuración de correo (variables de entorno). Ejemplo con Gmail:
# SMTP_HOST=smtp.gmail.com  SMTP_USER=tucorreo@gmail.com  SMTP_PASS=<contraseña de aplicación>
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with db() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                correo TEXT UNIQUE,
                clave_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tokens_reset (
                token_hash TEXT PRIMARY KEY,
                usuario_id INTEGER NOT NULL,
                expira TEXT NOT NULL
            );
        """)


def migrar():
    """Convierte la tabla vieja (usuario, clave en texto plano) a la nueva con hashes.
    HAZ UNA COPIA DE tienda.db ANTES. Ejecutar una sola vez: python app.py migrar"""
    con = db()
    viejos = con.execute("SELECT usuario, clave FROM usuarios").fetchall()
    con.executescript("""
        DROP TABLE IF EXISTS usuarios_nueva;
        CREATE TABLE usuarios_nueva (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            correo TEXT UNIQUE,
            clave_hash TEXT NOT NULL
        );
    """)
    for u in viejos:
        con.execute(
            "INSERT INTO usuarios_nueva (usuario, clave_hash) VALUES (?, ?)",
            (u["usuario"], generate_password_hash(u["clave"])),
        )
    con.executescript("""
        DROP TABLE usuarios;
        ALTER TABLE usuarios_nueva RENAME TO usuarios;
    """)
    con.commit()
    con.close()
    print(f"Migrados {len(viejos)} usuarios. Las contraseñas en texto plano ya no existen.")


def enviar_correo(destino, asunto, cuerpo):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = destino
    msg["Subject"] = asunto
    msg.set_content(cuerpo)
    with smtplib.SMTP_SSL(SMTP_HOST, 465) as s:
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


# ---------- Plantillas mínimas ----------
BASE = """
<!doctype html><meta charset="utf-8"><title>Tienda</title>
{% with msgs = get_flashed_messages() %}{% for m in msgs %}<p><b>{{ m }}</b></p>{% endfor %}{% endwith %}
{{ contenido|safe }}
"""

def pagina(html):
    return render_template_string(BASE, contenido=html)


# ---------- Rutas ----------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        correo = request.form["correo"].strip().lower()
        clave = request.form["clave"]

        if not usuario or "@" not in correo or len(clave) < 8:
            flash("Revisa los datos: la contraseña debe tener al menos 8 caracteres.")
            return redirect(url_for("registro"))
        try:
            with db() as con:
                con.execute(
                    "INSERT INTO usuarios (usuario, correo, clave_hash) VALUES (?, ?, ?)",
                    (usuario, correo, generate_password_hash(clave)),
                )
        except sqlite3.IntegrityError:
            flash("Ese usuario o correo ya está registrado.")
            return redirect(url_for("registro"))
        flash("Cuenta creada. Ya puedes iniciar sesión.")
        return redirect(url_for("login"))

    return pagina("""
        <h2>Crear cuenta</h2>
        <form method="post">
          <input name="usuario" placeholder="Usuario" required><br>
          <input name="correo" type="email" placeholder="Correo" required><br>
          <input name="clave" type="password" placeholder="Contraseña (mín. 8)" required><br>
          <button>Registrarme</button>
        </form>
        <a href="/login">Ya tengo cuenta</a>
    """)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        clave = request.form["clave"]
        with db() as con:
            fila = con.execute(
                "SELECT id, clave_hash FROM usuarios WHERE usuario = ?", (usuario,)
            ).fetchone()
        if fila and check_password_hash(fila["clave_hash"], clave):
            session.clear()
            session["usuario_id"] = fila["id"]
            return redirect("/")
        flash("Usuario o contraseña incorrectos.")
        return redirect(url_for("login"))

    return pagina("""
        <h2>Iniciar sesión</h2>
        <form method="post">
          <input name="usuario" placeholder="Usuario" required><br>
          <input name="clave" type="password" placeholder="Contraseña" required><br>
          <button>Entrar</button>
        </form>
        <a href="/olvide">Olvidé mi contraseña</a> · <a href="/registro">Crear cuenta</a>
    """)


@app.route("/olvide", methods=["GET", "POST"])
def olvide():
    if request.method == "POST":
        correo = request.form["correo"].strip().lower()
        with db() as con:
            fila = con.execute(
                "SELECT id FROM usuarios WHERE correo = ?", (correo,)
            ).fetchone()
            if fila:
                token = secrets.token_urlsafe(32)
                expira = (datetime.utcnow() + timedelta(minutes=30)).isoformat()
                con.execute("DELETE FROM tokens_reset WHERE usuario_id = ?", (fila["id"],))
                con.execute(
                    "INSERT INTO tokens_reset (token_hash, usuario_id, expira) VALUES (?, ?, ?)",
                    (hash_token(token), fila["id"], expira),
                )
                enlace = url_for("reset", token=token, _external=True)
                try:
                    enviar_correo(
                        correo,
                        "Recupera tu contraseña",
                        f"Entra a este enlace para crear una nueva contraseña "
                        f"(vence en 30 minutos):\n\n{enlace}\n\n"
                        f"Si no lo pediste tú, ignora este correo.",
                    )
                except Exception as e:
                    app.logger.error("Error enviando correo: %s", e)
        # Mismo mensaje exista o no el correo, para no revelar quién tiene cuenta
        flash("Si ese correo está registrado, te enviamos un enlace para recuperar tu contraseña.")
        return redirect(url_for("login"))

    return pagina("""
        <h2>Recuperar contraseña</h2>
        <form method="post">
          <input name="correo" type="email" placeholder="Tu correo" required><br>
          <button>Enviar enlace</button>
        </form>
    """)


@app.route("/reset/<token>", methods=["GET", "POST"])
def reset(token):
    th = hash_token(token)
    with db() as con:
        fila = con.execute(
            "SELECT usuario_id, expira FROM tokens_reset WHERE token_hash = ?", (th,)
        ).fetchone()
        valido = fila and datetime.fromisoformat(fila["expira"]) > datetime.utcnow()
        if not valido:
            flash("El enlace no es válido o ya venció. Pide uno nuevo.")
            return redirect(url_for("olvide"))

        if request.method == "POST":
            clave = request.form["clave"]
            if len(clave) < 8:
                flash("La contraseña debe tener al menos 8 caracteres.")
                return redirect(url_for("reset", token=token))
            con.execute(
                "UPDATE usuarios SET clave_hash = ? WHERE id = ?",
                (generate_password_hash(clave), fila["usuario_id"]),
            )
            con.execute("DELETE FROM tokens_reset WHERE usuario_id = ?", (fila["usuario_id"],))
            flash("Contraseña actualizada. Ya puedes entrar.")
            return redirect(url_for("login"))

    return pagina("""
        <h2>Nueva contraseña</h2>
        <form method="post">
          <input name="clave" type="password" placeholder="Nueva contraseña (mín. 8)" required><br>
          <button>Guardar</button>
        </form>
    """)


@app.route("/")
def inicio():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return pagina("<h2>¡Bienvenido a la tienda!</h2>")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "migrar":
        migrar()
    else:
        init_db()
        app.run(debug=False)
