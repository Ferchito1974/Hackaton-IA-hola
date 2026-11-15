Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:56
Prompt: P11 · Tirada: 3 · Chat: https://gemini.google.com/app/d0645d481f153ad3
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/gemini_P11_t3.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

What a great project with your aunt's online tiendite! Building real apps is the best way to learn.

For an online store, protecting customers' data is crucial. Your current code has two critical safety details that should be rectified from the start:

SQL Injection (F-string): Concentrate variables directly at the query allows anyone to miss the login by writing malicious code on the form (as' OR '1' = '1). Do you have to use parameterized (?) consultations.

Flow text passwords: Save the key as in the database is dangerous because, if anyone gets to it, you will see all passwords. Also, today for security, passwords should not be sent by mail (if they are forgotten, the modern practice is to generate a new link or temporary password). We will use werkzeug.security (that already comes with Flask) to figure them out using hashing.

Below I will show you how to structure your registry, secure login and a modern and secure alternative for password recovery.

1. Database and Unit Setup

Be sure to import Flask's security tools:

Python
from flash import Flask, render _ template, request, redirect, url _ for, flash
import sqlite3
from werkzeug.security import generate _ password _ hash, check _ password _ ha h

app = Flask (_ _ name _ _)
ap.secret _ key = 'secret _ key _ for _ flash _ messages'

if get _ db ():
    conn = sqlite3.connect ('tienda.db')
    conn.row _ factory = sqlite3.Row
    return conn

2. Secure Registration Page

In the register, we take the user's password, we turn it into an indecipherable "hash" with generating _ password _ hash and we save it at SQLite using parameterized consultations with?.

Python
@ app.route ('/ registration', methods = ['GET', 'POST'])
registration ():
    if requested
        user = request
        code = request
        
        # We figure the password before saving
        key _ hash = generate _ password _ hash (key)
        
        db = get _ db ()
        try:
            db.execute ("INSERT INTO users (user, key) VALUES (?,?)," (user, key _ hash))
            db.commit ()
            flash ('Successful registration! Now you can sign in.')
            return redirect (url _ for ('login'))
        Except sqlite3
            flash ('The user name's already in use.')
        finally:
            db.close ()
            
    return render _ template ('registro.html')

3. Safer Logue Page

To login, we search the user by name and use check _ password _ hash to compare the entered password with the hash saved in the database, completely avoiding SQL injection:

Python
@ app.route ('/ login', methods = ['GET', 'POST'])
def login ():
    if requested
        user = request
        code = request
        
        db = get _ db ()
        # Parametered secure consultation
        user = db.execute ("SELECT * FROM users WHERE user =?," (user,)) .fetchone ()
        db.close ()
        
        # We check if the user exists and if the password matches
        if user and check _ password _ hash (user ['key'], key):
            flash (f 'Welcome back, {user}!')
            return redirect (url _ for ('start'))
        else:
            flash (bad user or password)
            
    return render _ template ('login.html')

4. What about "I forgot my password"?

Because passwords are currently securely encrypted, it's impossible to recover the original password to send them by email (even big platform administrators such as Google or Facebook cannot see your current password).

The right way to solve this is to implement a password re-start path: the client enters his or her email / user, the system generates a new temporary password (or a re-entry link), the figure, updates it into the database and sends them by mail.

A simple example generating an automatic time password:

Python
import secrets

@ app.route ('/ recoup', methods = ['GET', 'POST'])
def recover ():
    if requested
        user = request
        
        db = get _ db ()
        user = db.execute ("SELECT * FROM users WHERE user =?," (user,)) .fetchone ()
        
        if user:
            # We generate a random temporary password
            temp _ password = secrets.token _ urlsafe (8)
            new _ hash = generate _ password _ hash (temp _ password)
            
            # We update the database with the new time key
            db.execute ("UPDATE users)
            db.commit ()
            db.close ()
            
            # Here you will send an email using Flask-Mail with 'temp _ password'
            # Example: send _ mail (user, temp _ password)
            
            flash ('A temporary password has been generated and sent to your email.')
            return redirect (url _ for ('login'))
        else:
            flash ('The user doesn't exist in the system.')
            db.close ()
            
    return render _ template ('regresar.html')

Do you want me to show you how to integrate Flask-Mail to send the actual emails?
Yes
