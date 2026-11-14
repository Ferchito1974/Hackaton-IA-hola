import os
import sqlite3
import smtplib
from email.message import EmailMessage

from flask import (Flask, request, redirect, url_for, session,
                   render_template_string, flash, g)
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------------------------------------------------------
# Configuración (usa variables de entorno, no pongas secretos en el código)
#   export SECRET_KEY="una-cadena-larga-y-aleatoria"
#   export SMTP_HOST="smtp.gmail.com"  SMTP_PORT="587"
#   export SMTP_USER="tucorreo@gmail.com"  SMTP_PASS="contraseña-de-aplicación"
# ---------------------------------------------------------------
app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
DB = "tienda.db"
serializer = URLSafeTimedSerializer(app.secret_key)
TOKEN_VIDA = 3600  # el enlace de recuperación dura 1 hora


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def cerrar_db(_):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                correo TEXT UNIQUE NOT NULL,
                clave_hash TEXT NOT NULL
            )""")


def enviar_correo(destino, asunto, cuerpo):
    msg = EmailMessage()
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = destino
    msg["Subject"] = asunto
    msg.set_content(cuerpo)
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", 587))) as s:
        s.starttls()
        s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        s.send_message(msg)


# ---------------------------------------------------------------
# Plantilla mínima (reemplázala por tus propios templates)
# ---------------------------------------------------------------
BASE = """
<!doctype html><meta charset="utf-8"><title>Tienda</title>
{% with msgs = get_flashed_messages() %}{% for m in msgs %}<p><b>{{ m }}</b></p>{% endfor %}{% endwith %}
<h2>{{ titulo }}</h2>
<form method="post">
  {% for nombre, tipo, etiqueta in campos %}
    <p><label>{{ etiqueta }}<br><input name="{{ nombre }}" type="{{ tipo }}" required></label></p>
  {% endfor %}
  <button>{{ boton }}</button>
</form>
{{ extra|safe }}
"""


def pagina(titulo, campos, boton, extra=""):
    return render_template_string(BASE, titulo=titulo, campos=campos, boton=boton, extra=extra)


# ---------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        correo = request.form["correo"].strip().lower()
        clave = request.form["clave"]
        if len(clave) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.")
        else:
            try:
                get_db().execute(
                    "INSERT INTO usuarios (usuario, correo, clave_hash) VALUES (?, ?, ?)",
                    (usuario, correo, generate_password_hash(clave)),
                )
                get_db().commit()
                flash("Cuenta creada. Ya puedes iniciar sesión.")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Ese usuario o correo ya está registrado.")
    return pagina("Crear cuenta",
                  [("usuario", "text", "Usuario"), ("correo", "email", "Correo"),
                   ("clave", "password", "Contraseña (mín. 8 caracteres)")],
                  "Registrarme")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        clave = request.form["clave"]
        # Consulta parametrizada: los valores nunca se mezclan con el SQL
        fila = get_db().execute(
            "SELECT id, clave_hash FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()
        if fila and check_password_hash(fila["clave_hash"], clave):
            session.clear()
            session["usuario_id"] = fila["id"]
            return redirect(url_for("inicio"))
        flash("Usuario o contraseña incorrectos.")
    return pagina("Iniciar sesión",
                  [("usuario", "text", "Usuario"), ("clave", "password", "Contraseña")],
                  "Entrar",
                  extra='<p><a href="/olvide">¿Olvidaste tu contraseña?</a> · '
                        '<a href="/registro">Crear cuenta</a></p>')


@app.route("/olvide", methods=["GET", "POST"])
def olvide():
    if request.method == "POST":
        correo = request.form["correo"].strip().lower()
        fila = get_db().execute(
            "SELECT id, clave_hash FROM usuarios WHERE correo = ?", (correo,)
        ).fetchone()
        if fila:
            # El token incluye un fragmento del hash actual: al cambiar la
            # contraseña, el enlace deja de servir (un solo uso).
            token = serializer.dumps([fila["id"], fila["clave_hash"][-10:]], salt="reset")
            enlace = url_for("restablecer", token=token, _external=True)
            try:
                enviar_correo(correo, "Recupera tu contraseña",
                              f"Entra a este enlace para elegir una nueva contraseña "
                              f"(vale 1 hora):\n\n{enlace}\n\n"
                              f"Si no lo pediste, ignora este correo.")
            except Exception:
                app.logger.exception("No se pudo enviar el correo")
        # Mismo mensaje exista o no el correo, para no revelar quién tiene cuenta
        flash("Si el correo está registrado, te enviamos un enlace.")
        return redirect(url_for("login"))
    return pagina("Recuperar contraseña", [("correo", "email", "Tu correo")], "Enviar enlace")


@app.route("/restablecer/<token>", methods=["GET", "POST"])
def restablecer(token):
    try:
        uid, huella = serializer.loads(token, salt="reset", max_age=TOKEN_VIDA)
    except (BadSignature, SignatureExpired):
        flash("El enlace no es válido o ya expiró.")
        return redirect(url_for("olvide"))

    fila = get_db().execute("SELECT clave_hash FROM usuarios WHERE id = ?", (uid,)).fetchone()
    if not fila or fila["clave_hash"][-10:] != huella:
        flash("Este enlace ya fue usado.")
        return redirect(url_for("olvide"))

    if request.method == "POST":
        clave = request.form["clave"]
        if len(clave) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.")
        else:
            get_db().execute("UPDATE usuarios SET clave_hash = ? WHERE id = ?",
                             (generate_password_hash(clave), uid))
            get_db().commit()
            flash("Contraseña actualizada. Inicia sesión.")
            return redirect(url_for("login"))
    return pagina("Nueva contraseña", [("clave", "password", "Nueva contraseña")], "Guardar")


@app.route("/")
def inicio():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return "Sesión iniciada. <a href='/salir'>Salir</a>"


@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------
# Migración: ejecuta UNA vez si ya tienes usuarios con clave en texto plano
#   python app.py migrar
# (Asume tabla vieja con columnas usuario, clave; agrega correo manualmente después.)
# ---------------------------------------------------------------
def migrar():
    with sqlite3.connect(DB) as con:
        cols = [c[1] for c in con.execute("PRAGMA table_info(usuarios)")]
        if "clave_hash" not in cols:
            con.execute("ALTER TABLE usuarios ADD COLUMN clave_hash TEXT")
        if "correo" not in cols:
            con.execute("ALTER TABLE usuarios ADD COLUMN correo TEXT")
        for uid, clave in con.execute(
                "SELECT id, clave FROM usuarios WHERE clave IS NOT NULL").fetchall():
            con.execute("UPDATE usuarios SET clave_hash = ?, clave = NULL WHERE id = ?",
                        (generate_password_hash(clave), uid))
    print("Listo: contraseñas convertidas a hash.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "migrar":
        migrar()
    else:
        init_db()
        app.run(debug=False)

