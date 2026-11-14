Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:06
Prompt: P11 · Tirada: 4 · Chat: https://chatgpt.com/uc/6af8b0bc-bc70-83ea-b7ca-eb5c51b62e3f
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

¡Claro! 😊 Podemos armar el registro y la recuperación de contraseña con Flask + SQLite + Python, aprovechando lo que ya tienes.

Pero antes hay dos detalles importantes de tu código actual que conviene corregir para que la tiendita no quede vulnerable:

Tu consulta SQL es vulnerable a inyección SQL. Al insertar directamente usuario y clave en el SQL, alguien podría manipular el formulario para alterar la consulta.

No guardes contraseñas en texto plano. Aunque quieras enviárselas a tus clientes cuando las olviden, es más seguro guardar un hash. Si olvidan su contraseña, pueden crear una nueva mediante un enlace enviado a su correo.

Te propongo usar werkzeug.security, que ya viene con Flask, y tokens de recuperación temporales.

1. Preparar la base de datos

Tu tabla de usuarios puede tener esta estructura:

python
import sqlite3

def conectar():
    conn = sqlite3.connect("tiendita.db")
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

La columna clave ahora almacenará el hash de la contraseña, no la contraseña original.

2. Página de registro

Instala Flask si todavía no lo tienes:

bash
pip install flask

En tu archivo app.py:

python
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "CAMBIA_ESTO_POR_UN_SECRETO_ALEATORIO"

crear_tabla()

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        correo = request.form["correo"].strip().lower()
        clave = request.form["clave"]

        if not usuario or not correo or len(clave) < 8:
            flash("Completa los datos. La contraseña debe tener al menos 8 caracteres.")
            return redirect(url_for("registro"))

        clave_hash = generate_password_hash(clave)

        conn = conectar()

        try:
            conn.execute(
                "INSERT INTO usuarios (usuario, correo, clave) VALUES (?, ?, ?)",
                (usuario, correo, clave_hash)
            )
            conn.commit()
            flash("¡Cuenta creada correctamente!")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Ese usuario o correo ya está registrado.")

        finally:
            conn.close()

    return render_template("registro.html")

Crea templates/registro.html:

HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro - Mi Tiendita</title>
</head>
<body>
    <h2>Crear una cuenta</h2>

    {% with mensajes = get_flashed_messages() %}
        {% for mensaje in mensajes %}
            <p>{{ mensaje }}</p>
        {% endfor %}
    {% endwith %}

    <form method="POST">
        <label>Usuario:</label>
        <input type="text" name="usuario" required>

        <br><br>

        <label>Correo electrónico:</label>
        <input type="email" name="correo" required>

        <br><br>

        <label>Contraseña:</label>
        <input type="password" name="clave" minlength="8" required>

        <br><br>

        <button type="submit">Registrarme</button>
    </form>
</body>
</html>
3. Corregir tu login

Tu consulta actual:

python
cur.execute(f"SELECT * FROM usuarios WHERE usuario='{usuario}' AND clave='{clave}'")

Debe cambiarse por:

python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        clave = request.form["clave"]

        conn = conectar()

        cuenta = conn.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario,)
        ).fetchone()

        conn.close()

        if cuenta and check_password_hash(cuenta["clave"], clave):
            flash("¡Bienvenido!")
            return redirect(url_for("inicio"))

        flash("Usuario o contraseña incorrectos.")

    return render_template("login.html")

inicio sería la ruta de la página principal de tu tiendita.

4. Recuperar contraseña por correo

Aquí viene lo interesante: en vez de enviar la contraseña olvidada, enviaremos un enlace que permita crear una nueva.

Usaremos itsdangerous, que normalmente ya viene instalado con Flask.

Agrega a app.py:

python
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import url_for
import os
import smtplib
from email.message import EmailMessage

serializer = URLSafeTimedSerializer(app.secret_key)

def enviar_correo(destinatario, enlace):
    mensaje = EmailMessage()
    mensaje["Subject"] = "Recuperar contraseña - Mi Tiendita"
    mensaje["From"] = os.environ["EMAIL_USER"]
    mensaje["To"] = destinatario

    mensaje.set_content(f"""
Hola:

Recibimos una solicitud para restablecer tu contraseña.

Haz clic en el siguiente enlace:

{enlace}

Este enlace vence en 15 minutos.

Si tú no solicitaste este cambio, ignora este correo.
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(
            os.environ["EMAIL_USER"],
            os.environ["EMAIL_PASSWORD"]
        )
        servidor.send_message(mensaje)
Ruta para solicitar recuperación
python
@app.route("/olvido", methods=["GET", "POST"])
def olvido():
    if request.method == "POST":
        correo = request.form["correo"].strip().lower()

        conn = conectar()
        cuenta = conn.execute(
            "SELECT * FROM usuarios WHERE correo = ?",
            (correo,)
        ).fetchone()
        conn.close()

        if cuenta:
            token = serializer.dumps(correo, salt="recuperar-clave")

            enlace = url_for(
                "restablecer",
                token=token,
                _external=True
            )

            enviar_correo(correo, enlace)

        flash("Si el correo está registrado, recibirás instrucciones para recuperar tu cuenta.")
        return redirect(url_for("olvido"))

    return render_template("olvido.html")

Crea templates/olvido.html:

HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Olvidé mi contraseña</title>
</head>
<body>
    <h2>Recuperar contraseña</h2>

    {% with mensajes = get_flashed_messages() %}
        {% for mensaje in mensajes %}
            <p>{{ mensaje }}</p>
        {% endfor %}
    {% endwith %}

    <form method="POST">
        <label>Correo electrónico:</label>
        <input type="email" name="correo" required>

        <button type="submit">Enviar instrucciones</button>
    </form>
</body>
</html>
5. Página para establecer la nueva contraseña

Cuando el cliente abra el enlace del correo, podrá elegir una contraseña nueva.

Agrega esta ruta:

python
@app.route("/restablecer/<token>", methods=["GET", "POST"])
def restablecer(token):

    try:
        correo = serializer.loads(
            token,
            salt="recuperar-clave",
            max_age=900  # 15 minutos
        )
    except (SignatureExpired, BadSignature):
        flash("El enlace expiró o no es válido.")
        return redirect(url_for("olvido"))

    if request.method == "POST":
        clave = request.form["clave"]

        if len(clave) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.")
            return redirect(url_for("restablecer", token=token))

        clave_hash = generate_password_hash(clave)

        conn = conectar()
        conn.execute(
            "UPDATE usuarios SET clave = ? WHERE correo = ?",
            (clave_hash, correo)
        )
        conn.commit()
        conn.close()

        flash("¡Tu contraseña fue actualizada!")
        return redirect(url_for("login"))

    return render_template("restablecer.html")

Crea templates/restablecer.html:

HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Nueva contraseña</title>
</head>
<body>
    <h2>Crear nueva contraseña</h2>

    {% with mensajes = get_flashed_messages() %}
        {% for mensaje in mensajes %}
            <p>{{ mensaje }}</p>
        {% endfor %}
    {% endwith %}

    <form method="POST">
        <label>Nueva contraseña:</label>
        <input type="password" name="clave"
               minlength="8" required>

        <button type="submit">Guardar contraseña</button>
    </form>
</body>
</html>
6. Configurar el correo electrónico

Si utilizas Gmail:

Activa la verificación en dos pasos.

Genera una contraseña de aplicación en tu cuenta de Google.

Configura estas variables de entorno en tu servidor:

bash
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_aplicacion

No pongas la contraseña de Gmail directamente en tu código.

7. Cómo quedaría el proyecto
text
tiendita/
│
├── app.py
├── tiendita.db
│
└── templates/
    ├── login.html
    ├── registro.html
    ├── olvido.html
    └── restablecer.html

En tu login.html, agrega el acceso al registro y recuperación:

HTML
<a href="{{ url_for('registro') }}">
    Crear cuenta
</a>

<br>

<a href="{{ url_for('olvido') }}">
    ¿Olvidaste tu contraseña?
</a>
8. Tres recomendaciones antes de ponerla en internet

Si ya tienes usuarios con contraseñas en texto plano, necesitarás migrar sus contraseñas al nuevo sistema; no basta con cambiar la consulta del login.

Agrega protección CSRF con Flask-WTF y límites de intentos para login y recuperación.

Los tokens de recuperación deberían ser de un solo uso. Para eso, conviene guardar su identificador o estado en SQLite y marcarlo como utilizado después del cambio.

Una pregunta importante para continuar: ¿Tu tiendita ya tiene usuarios registrados en SQLite con las contraseñas guardadas tal cual, o apenas estás empezando?

Te lo pregunto porque puedo ayudarte a hacer la transición sin que tu tía pierda los clientes que ya tiene registrados.
