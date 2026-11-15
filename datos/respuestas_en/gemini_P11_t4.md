Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:57
Prompt: P11 · Tirada: 4 · Chat: https://gemini.google.com/app/d5f9f983e6fd2e2c
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/gemini_P11_t4.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

What a great project you're doing for your aunt! To help digitise a family business is excellent.

Before viewing registration and mail, there are a few very important security details in your current code that's worth adjusting from now on. Using F-strings to put together SQL queries (cur.execute (f...)) leave the tiendite exposed to SQL Injection, where someone could enter without password or erase the database by writing commands to the form. Also, saving passwords into flat text is dangerous: if anyone gets to see the database, they will know the key to all customers (and many use the same key to their bench or mail).

The best practice is to use parametered consultations (to avoid injections) and passwords hacking (save an encryption code that cannot be reversed). That's why the modern standard for "I forgot my password" isn't sending the current key by email (because nobody, even you, should be able to read it) but sending a link to re-establish it.

Here's how to safely structure the registry, login and database using Flask and SQLite:

1. Prepare database and registry

First, be sure to import the security tools that Flask already brings (werkzeug.security).

Python
from flask import Flask, render _ template, request, redirect, url _ for, session, flash
from werkzeug.security import generate _ password _ hash, check _ password _ ha h
import sqlite3

app = Flask (_ _ name _ _)
ap.secret _ key = 'your _ key _ secret _ here' # necessary for flash messages

if get _ db _ connection ():
    conn = sqlite3.connect ('tienda.db')
    conn.row _ factory = sqlite3.Row
    return conn

# To create a table if it doesn't exist
If init _ db ():
    conn = get _ db _ connection ()
    conn.execute (')
        CREATE TABLE IF NOT EXIST users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT UNIQUE NOT NULL,
            TEXT NOT NULL,
            TEXT NOT NULL key
        )
    ''')
    conn.commit ()
    conn.close ()

init _ db ()

Registration path (/ registration)

Here we use to generate _ password _ hash to secure your password.

Python
@ app.route ('/ registration', methods = ['GET', 'POST'])
registration ():
    if requested
        user = request
        Email = request
        code = request
        
        # We have entered the password before saving it
        code _ cipher = generate _ password _ hash (key)
        
        conn = get _ db _ connection ()
        try:
            _
            conn.execute (
                "INSERT INTO users (user, mail, key) VALES (?,?,?),"
                (user, email, code _ cipher)
            )
            conn.commit ()
            flash ('Successful registration! Now you can login.', 'success')
            return redirect (url _ for ('login'))
        Except sqlite3
            flash ('The username's already in use.', 'error')
        finally:
            conn.close ()
            
    return render _ template ('registro.html')

2. Lozo Seguro

Your login will now use check _ password _ hash to compare the entered password with the encrypted version saved in the database, using also a parameterized (?) query.

Python
@ app.route ('/ login', methods = ['GET', 'POST'])
def login ():
    if requested
        user = request
        code = request
        
        conn = get _ db _ connection ()
        ♪ Safe consultation with '?
        user = conn.execute (
            "SELECT * FROM users WHERE user =?,"
            (user)
        ) .fetchone ()
        conn.close ()
        
        # We check if the user exists and if the password matches
        if user and check _ password _ hash (user ['key'], key):
            session ['user'] = user ['user']
            flash ('Welcome back!', 'success')
            return redirect (url _ for ('dashboard')) # Or the main tent page
        else:
            flash (bad user or password.)
            
    return render _ template ('login.html')

3. "I forgot my password" button (Secure Flow)

To implement this by sending an email, you can use the Flask-Mail extension. Instead of revealing the current password, the system generates a unique (token) identifier, creates a time link and sends it to the client's email.

Install Flask-Mail at your terminal: pip install Flask-Mail

Configure the email in your application:

Python
from flask _ mail import Mail, message
import uuid # To generate unique recovery code

ap.config ['MAIL _ SERVER'] = 'smtp.gmail.com'
app.config ['MAIL _ PORT'] = 587
app.config ['MAIL _ USE _ TLS'] = True
app.config ['MAIL _ USERNAME'] = 'tumail @ gmail.com'
app.config ['MAIL _ PASSWORD'] = 'your _ password _ from _ application _ from _ google'
Email = Mail (app)


You can add a temporary column to your user table called token _ recovery and create a path to demand change:

Python
@ app.route ('/ recoup', methods = ['GET', 'POST'])
def recover ():
    if requested
        Email = request
        
        conn = get _ db _ connection ()
        user = conn.execute ("SELECT * FROM users WHERE mail =?," (mail,)) .fetchone ()
        
        if user:
            # We generate a unique recovery token
            token = str (uuid.uid4 ())
            conn.execute ("UPDATE users SET token _ recovery =? WHERE mail =?," (token, mail))
            conn.commit ()
            
            # Link that the user will get
            link = url _ for ('reset', token = token, _ external = True)
            
            # We send the mail
            Mg = Message ('Password Recovery - Stretch'),
                          sender = 'tumail @ gmail.com',
                          recipients = [mail])
            Ms.body = f'Hello, have requested to restore your password. Enter the following link to create a new:
            mail.send (msg)
            
            flash ('We have sent you an email with instructions.', 'info')
        else:
            flash ('We did not find an account associated with that email.', 'error')
            
        conn.close ()
    return render _ template ('regresar.html')

@ app.route ('/ reset / < token >', methods = ['GET', 'POST'])
of re-establishing (token):
    if requested
        new _ key = request
        code _ cipher = generate _ password _ hash (new _ key)
        
        conn = get _ db _ connection ()
        # We search for the user by token and update the password by cleaning the token
        user = conn.execute ("SELECT * FROM users WHere token _ recovery =?," (token,)) .fetchone ()
        
        if user:
            conn.execute ("UPDATE users set key =?, token _ recovery = NULL WHere id =?,"
                         (code _ cipher, user ['id'))
            conn.commit ()
            conn.close ()
            flash ('Password updated with success. Now you can login.', 'success')
            return redirect (url _ for ('login'))
        else:
            conn.close ()
            flash ('The link is invalid or has expired.', 'error')
            
    return render _ template ('re-established .html')

Do you want me to show you how to put together the simple HTML forms for these routes?
Yes
