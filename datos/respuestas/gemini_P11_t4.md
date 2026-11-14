Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:57
Prompt: P11 · Tirada: 4 · Chat: https://gemini.google.com/app/d5f9f983e6fd2e2c
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

¡Qué gran proyecto estás haciendo para tu tía! Ayudar a digitalizar un negocio familiar es excelente.

Antes de ver el registro y el correo, hay un par de detalles de seguridad muy importantes en tu código actual que vale la pena ajustar desde ya. Usar f-strings para armar consultas SQL (cur.execute(f"...")) deja la tiendita expuesta a Inyección SQL, donde alguien podría entrar sin contraseña o borrar la base de datos escribiendo comandos en el formulario. Además, guardar las contraseñas en texto plano es peligroso: si alguien llega a ver la base de datos, sabrá la clave de todos los clientes (y muchos usan la misma clave en su banco o correo).

La buena práctica es usar consultas parametrizadas (para evitar inyecciones) y hashing de contraseñas (guardar un código cifrado que no se puede revertir). Por esta razón, el estándar moderno para "olvidé mi contraseña" no es mandar la clave actual por correo (porque nadie, ni siquiera tú, debería poder leerla), sino enviar un enlace para restablecerla.

Aquí tienes cómo estructurar de forma segura el registro, el login y la base de datos usando Flask y SQLite:

1. Preparar la Base de Datos y el Registro

Primero, asegúrate de importar las herramientas de seguridad que ya trae Flask (werkzeug.security).

Python
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui' # Necesaria para los mensajes flash

def get_db_connection():
    conn = sqlite3.connect('tienda.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla si no existe
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            correo TEXT NOT NULL,
            clave TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

Ruta de Registro (/registro)

Aquí usamos generate_password_hash para que la contraseña se guarde protegida.

Python
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        correo = request.form['correo']
        clave = request.form['clave']
        
        # Encriptamos la contraseña antes de guardarla
        clave_cifrada = generate_password_hash(clave)
        
        conn = get_db_connection()
        try:
            # CONSULTA PARAMETRIZADA (Protegida contra SQL Injection con los signos '?')
            conn.execute(
                "INSERT INTO usuarios (usuario, correo, clave) VALUES (?, ?, ?)",
                (usuario, correo, clave_cifrada)
            )
            conn.commit()
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya está en uso.', 'error')
        finally:
            conn.close()
            
    return render_template('registro.html')

2. Login Seguro

Tu login ahora usará check_password_hash para comparar la contraseña ingresada con la versión cifrada guardada en la base de datos, utilizando también una consulta parametrizada (?).

Python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        conn = get_db_connection()
        # Consulta segura con '?'
        user = conn.execute(
            "SELECT * FROM usuarios WHERE usuario = ?", 
            (usuario,)
        ).fetchone()
        conn.close()
        
        # Verificamos si el usuario existe y si la contraseña coincide
        if user and check_password_hash(user['clave'], clave):
            session['usuario'] = user['usuario']
            flash('¡Bienvenido de nuevo!', 'success')
            return redirect(url_for('dashboard')) # O la página principal de la tienda
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
            
    return render_template('login.html')

3. Botón de "Olvidé mi contraseña" (Flujo Seguro)

Para implementar esto enviando un correo electrónico, puedes usar la extensión Flask-Mail. En lugar de revelar la contraseña actual, el sistema genera un identificador único (token), crea un enlace temporal y se lo envía al correo del cliente.

Instala Flask-Mail en tu terminal: pip install Flask-Mail

Configura el correo en tu aplicación:

Python
from flask_mail import Mail, Message
import uuid # Para generar códigos únicos de recuperación

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tucorreo@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_contraseña_de_aplicacion_de_google'
mail = Mail(app)


Puedes agregar una columna temporal a tu tabla de usuarios llamada token_recuperacion y crear una ruta para solicitar el cambio:

Python
@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        correo = request.form['correo']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,)).fetchone()
        
        if user:
            # Generamos un token único de recuperación
            token = str(uuid.uuid4())
            conn.execute("UPDATE usuarios SET token_recuperacion = ? WHERE correo = ?", (token, correo))
            conn.commit()
            
            # Enlace que recibirá el usuario
            enlace = url_for('restablecer', token=token, _external=True)
            
            # Enviamos el correo
            msg = Message('Recuperación de contraseña - Tiendita',
                          sender='tucorreo@gmail.com',
                          recipients=[correo])
            msg.body = f'Hola, haz solicitado restablecer tu contraseña. Entra al siguiente enlace para crear una nueva:\n\n{enlace}'
            mail.send(msg)
            
            flash('Te hemos enviado un correo con las instrucciones.', 'info')
        else:
            flash('No encontramos una cuenta asociada a ese correo.', 'error')
            
        conn.close()
    return render_template('recuperar.html')

@app.route('/restablecer/<token>', methods=['GET', 'POST'])
def restablecer(token):
    if request.method == 'POST':
        nueva_clave = request.form['clave']
        clave_cifrada = generate_password_hash(nueva_clave)
        
        conn = get_db_connection()
        # Buscamos al usuario por el token y actualizamos la contraseña limpiando el token
        user = conn.execute("SELECT * FROM usuarios WHERE token_recuperacion = ?", (token,)).fetchone()
        
        if user:
            conn.execute("UPDATE usuarios SET clave = ?, token_recuperacion = NULL WHERE id = ?", 
                         (clave_cifrada, user['id']))
            conn.commit()
            conn.close()
            flash('Contraseña actualizada con éxito. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            conn.close()
            flash('El enlace es inválido o ha expirado.', 'error')
            
    return render_template('restablecer.html')

¿Quieres que te muestre cómo armar los formularios HTML sencillos para estas rutas?
Sí
