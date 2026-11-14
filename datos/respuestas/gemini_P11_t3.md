Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:56
Prompt: P11 · Tirada: 3 · Chat: https://gemini.google.com/app/d0645d481f153ad3
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

¡Qué gran proyecto el de la tiendita en línea de tu tía! Construir aplicaciones reales es la mejor forma de aprender.

Para una tienda en línea, proteger los datos de los clientes es fundamental. Tu código actual tiene dos detalles críticos de seguridad que conviene corregir desde el inicio:

Inyección SQL (f-string): Concatenar variables directamente en la consulta permite que cualquiera pueda saltarse el login escribiendo código malicioso en el formulario (como ' OR '1'='1). Debes usar consultas parametrizadas (?).

Contraseñas en texto plano: Guardar la clave tal cual en la base de datos es peligroso porque, si alguien accede a ella, verá todas las contraseñas. Además, hoy en día por seguridad no se deben enviar contraseñas por correo (si se olvidan, la práctica moderna es generar un enlace o una contraseña temporal nueva). Usaremos werkzeug.security (que ya viene con Flask) para cifrarlas mediante hashing.

A continuación te muestro cómo estructurar el registro, el login seguro y una alternativa moderna y segura para la recuperación de contraseña.

1. Configuración de la Base de Datos y Dependencias

Asegúrate de importar las herramientas de seguridad de Flask:

Python
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash_messages'

def get_db():
    conn = sqlite3.connect('tienda.db')
    conn.row_factory = sqlite3.Row
    return conn

2. Página de Registro Segura

En el registro, tomamos la contraseña del usuario, la transformamos en un "hash" indescifrable con generate_password_hash y la guardamos en SQLite usando consultas parametrizadas con ?.

Python
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        # Ciframos la contraseña antes de guardarla
        clave_hash = generate_password_hash(clave)
        
        db = get_db()
        try:
            db.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", (usuario, clave_hash))
            db.commit()
            flash('¡Registro exitoso! Ya puedes iniciar sesión.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya está en uso.')
        finally:
            db.close()
            
    return render_template('registro.html')

3. Página de Login Segura

Para iniciar sesión, buscamos al usuario por su nombre y usamos check_password_hash para comparar la contraseña ingresada con el hash guardado en la base de datos, evitando por completo la inyección SQL:

Python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        db = get_db()
        # Consulta segura parametrizada
        user = db.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,)).fetchone()
        db.close()
        
        # Verificamos si el usuario existe y si la contraseña coincide
        if user and check_password_hash(user['clave'], clave):
            flash(f'¡Bienvenido de nuevo, {usuario}!')
            return redirect(url_for('inicio'))
        else:
            flash('Usuario o contraseña incorrectos.')
            
    return render_template('login.html')

4. ¿Qué hacemos con "Olvidé mi contraseña"?

Debido a que las contraseñas ahora están cifradas de forma segura, es imposible recuperar la contraseña original para enviarla por correo (incluso los administradores de grandes plataformas como Google o Facebook no pueden ver tu contraseña actual).

La forma correcta de resolver esto es implementar una ruta de reinicio de contraseña: el cliente ingresa su correo/usuario, el sistema genera una contraseña temporal nueva (o un enlace de restablecimiento), la cifra, la actualiza en la base de datos y se la envía por correo.

Un ejemplo sencillo generando una contraseña temporal automática:

Python
import secrets

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        usuario = request.form['usuario']
        
        db = get_db()
        user = db.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,)).fetchone()
        
        if user:
            # Generamos una contraseña temporal aleatoria
            temp_password = secrets.token_urlsafe(8)
            nuevo_hash = generate_password_hash(temp_password)
            
            # Actualizamos la base de datos con la nueva clave temporal
            db.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", (nuevo_hash, usuario))
            db.commit()
            db.close()
            
            # AQUÍ enviarías el correo electrónico usando Flask-Mail con 'temp_password'
            # Ejemplo: enviar_correo(usuario, temp_password)
            
            flash('Se ha generado una contraseña temporal y se ha enviado a tu correo.')
            return redirect(url_for('login'))
        else:
            flash('El usuario no existe en el sistema.')
            db.close()
            
    return render_template('recuperar.html')

¿Quieres que te muestre cómo integrar Flask-Mail para enviar los correos electrónicos reales?
Sí
