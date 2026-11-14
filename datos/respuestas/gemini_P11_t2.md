Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:55
Prompt: P11 · Tirada: 2 · Chat: https://gemini.google.com/app/7874f9ff44f87fdd
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

¡Qué gran proyecto estás armando para la tiendita de tu tía! Automatizar eso le va a ahorrar muchos dolores de cabeza.

Antes de ver el código, hay dos detalles clave de seguridad que vale la pena ajustar desde ya:

Inyección SQL: Usar f-strings (f"...") en las consultas a la base de datos permite que cualquiera escriba código malicioso en el campo de usuario y robe o borre la base de datos. Se soluciona usando consultas parametrizadas (?).

Contraseñas en texto plano: Guardar las claves tal cual es peligroso porque si alguien accede a la base de datos, ve las de todos. Para cumplir con tu idea de mandarles una contraseña por correo si la olvidan, la mejor práctica moderna es generar una contraseña temporal aleatoria, guardarla encriptada y enviarla por email. Así no guardas contraseñas reales en texto plano, pero el cliente recupera el acceso de inmediato.

Aquí tienes cómo estructurar tu aplicación en Flask de forma segura, incluyendo el registro, el login corregido y la recuperación de contraseña por correo.

1. Código principal en Flask (app.py)

Asegúrate de tener instalados Flask y Werkzeug (viene incluido con Flask para manejar la seguridad).

Python
import sqlite3
import random
import string
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'una_clave_secreta_muy_segura' # Necesario para usar flash messages

def init_db():
    conn = sqlite3.connect('tienda.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            email TEXT UNIQUE,
            clave TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inicializamos la base de datos al arrancar
init_db()

@app.route('/')
def home():
    if 'usuario' in session:
        return f"¡Hola {session['usuario']}! Bienvenid@ a la tienda de tu tía. <a href='/logout'>Cerrar sesión</a>"
    return redirect(url_for('login'))

# --- RUTA DE REGISTRO ---
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        clave = request.form['clave']
        
        # Encriptamos la contraseña para guardarla de forma segura
        clave_hash = generate_password_hash(clave)
        
        try:
            conn = sqlite3.connect('tienda.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (usuario, email, clave) VALUES (?, ?, ?)", 
                        (usuario, email, clave_hash))
            conn.commit()
            conn.close()
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario o correo ya están registrados.', 'danger')
            
    return render_template('registro.html')

# --- RUTA DE LOGIN (Segura contra Inyección SQL) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        conn = sqlite3.connect('tienda.db')
        cur = conn.cursor()
        # Usamos '?' para evitar Inyección SQL
        cur.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        user = cur.fetchone()
        conn.close()
        
        # user[1] = usuario, user[2] = email, user[3] = clave_hash
        if user and check_password_hash(user[3], clave):
            session['usuario'] = user[1]
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            
    return render_template('login.html')

# --- RUTA DE OLVIDÉ MI CONTRASEÑA ---
@app.route('/olvide-password', methods=['GET', 'POST'])
def olvide_password():
    if request.method == 'POST':
        email = request.form['email']
        
        conn = sqlite3.connect('tienda.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cur.fetchone()
        
        if user:
            # Generar una contraseña temporal aleatoria de 8 caracteres
            caracteres = string.ascii_letters + string.digits
            temp_password = ''.join(random.choice(caracteres) for _ in range(8))
            temp_hash = generate_password_hash(temp_password)
            
            # Actualizamos la contraseña en la base de datos
            cur.execute("UPDATE usuarios SET clave = ? WHERE email = ?", (temp_hash, email))
            conn.commit()
            conn.close()
            
            # Enviar correo electrónico
            try:
                msg = EmailMessage()
                msg.set_content(f'Hola! Has solicitado recuperar tu contraseña.\n\nTu nueva contraseña temporal es: {temp_password}\n\nTe recomendamos iniciar sesión y cambiarla por una que recuerdes.')
                msg['Subject'] = 'Recuperación de contraseña - Tiendita'
                msg['From'] = 'tucorreo@gmail.com' # Tu correo
                msg['To'] = email
                
                # Configuración SMTP (Ejemplo usando Gmail)
                # Nota: Para Gmail, necesitas generar una "Contraseña de aplicación" en tu cuenta de Google.
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login('tucorreo@gmail.com', 'tu_contrasena_de_aplicacion')
                    smtp.send_message(msg)
                    
                flash('Te hemos enviado una contraseña temporal a tu correo.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f'Error al enviar el correo. Inténtalo más tarde.', 'danger')
        else:
            conn.close()
            flash('El correo ingresado no está registrado.', 'danger')
            
    return render_template('olvide_password.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

2. Las Plantillas HTML (templates/)

Crea una carpeta llamada templates en el mismo directorio de tu script y coloca estos tres archivos básicos:

templates/login.html
HTML
<!DOCTYPE html>
<html lang="es">
<head><title>Login</title></head>
<body>
    <h2>Iniciar Sesión</h2>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul>
          {% for category, message in messages %}
            <li style="color: red;">{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    
    <form method="POST">
        <label>Usuario:</label><br>
        <input type="text" name="usuario" required><br><br>
        <label>Contraseña:</label><br>
        <input type="password" name="clave" required><br><br>
        <button type="submit">Entrar</button>
    </form>
    <p>¿No tienes cuenta? <a href="/registro">Regístrate aquí</a></p>
    <p><a href="/olvide-password">¿Olvidaste tu contraseña?</a></p>
</body>
</html>

templates/registro.html
HTML
<!DOCTYPE html>
<html lang="es">
<head><title>Registro</title></head>
<body>
    <h2>Registro de Usuario</h2>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul>
          {% for category, message in messages %}
            <li style="color: red;">{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    
    <form method="POST">
        <label>Usuario:</label><br>
        <input type="text" name="usuario" required><br><br>
        <label>Correo electrónico:</label><br>
        <input type="email" name="email" required><br><br>
        <label>Contraseña:</label><br>
        <input type="password" name="clave" required><br><br>
        <button type="submit">Registrarse</button>
    </form>
    <p>¿Ya tienes cuenta? <a href="/login">Inicia sesión</a></p>
</body>
</html>

templates/olvide_password.html
HTML
<!DOCTYPE html>
<html lang="es">
<head><title>Recuperar Contraseña</title></head>
<body>
    <h2>Recuperar Contraseña</h2>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul>
          {% for category, message in messages %}
            <li style="color: red;">{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    
    <p>Ingresa tu correo y te enviaremos una contraseña temporal:</p>
    <form method="POST">
        <label>Correo electrónico:</label><br>
        <input type="email" name="email" required><br><br>
        <button type="submit">Enviar nueva contraseña</button>
    </form>
    <p><a href="/login">Volver al login</a></p>
</body>
</html>

Notas importantes para el envío de correos:

Si usas Gmail para enviar los correos desde la app de tu tía, recuerda que Google ya no permite poner la contraseña normal de la cuenta en el código por seguridad. Debes ir a tu cuenta de Google, activar la verificación en dos pasos y generar una "Contraseña de aplicación" (App Password), la cual usarás en la línea smtp.login('tucorreo@gmail.com', 'tu_contrasena_de_aplicacion').
