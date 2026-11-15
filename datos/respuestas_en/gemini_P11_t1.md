Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:54
Prompt: P11 · Tirada: 1 · Chat: https://gemini.google.com/app/3842922f26e4ead5
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/gemini_P11_t1.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

What a great project you're doing for your aunt's tiendite! Before we set up registration and recovery, there are a few very important security details in your current code that we have to adjust to protect the tent:

SQL Injection: Using f... "directly with form data allows anyone to steal or erase your database by writing malicious code into the user field. It's solved using parametered (?) consultations.

Flow text passwords: Save passwords as they are dangerous because if anyone gets to the database, you will see the keys to all customers. Also, if the encryption (as should be), you will be unable to read them to send them by mail. The industry's standard solution is to generate and send a new temporary password (or a re-establishment link).

We're gonna structure all this safely using Flask, SQLite and Flask-Mail for emails.

1. Correct Login and secure database

First, make sure your table has an email column and that you save your encrypted passwords using werkzeug.security (that's already included with Flask).

Python
from flask import Flask, render _ template, request, redirect, url _ for, session
from werkzeug.security import generate _ password _ hash, check _ password _ ha h
import sqlite3

app = Flask (_ _ name _ _)

# Example database configuration
If init _ db ():
    conn = sqlite3.connect ('tienda.db')
    cur = conn.cursor ()
    cur.execute ("')
        CREATE TABLE IF NOT EXIST users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            TEXT NOT NULL key
        )
    ''')
    conn.commit ()
    conn.close ()

init _ db ()

@ app.route ('/ login', methods = ['POST'])
def login ():
    user = request
    code = request
    
    conn = sqlite3.connect ('tienda.db')
    cur = conn.cursor ()
    # Secure Consultation against SQL Injection using tuples (?)
    cur.execute ("FROM key SELECT users WHERE user =?," (user,))
    user = cur.fetchone ()
    conn.close ()
    
    # We check if user exists and if password matches hash
    if user and check _ password _ hash (user [0], key):
        return f "Welcome back, {user}!"
    return "User or wrong password."

2. Registration Page (/ registration)

Here we register the user by saving the encrypted password with generate _ password _ hash.

Flask path:

Python
@ app.route ('/ registration', methods = ['GET', 'POST'])
registration ():
    if requested
        user = request
        email = request
        code = request
        
        # We have entered the password before saving it
        key _ hash = generate _ password _ hash (key)
        
        try:
            conn = sqlite3.connect ('tienda.db')
            cur = conn.cursor ()
            cur.execute ("INSERT INTO users (user, email, key) VALUES (?,?,?)"
                        (user, email, key _ hash))
            conn.commit ()
            conn.close ()
            return redirect (url _ for ('login _ page')) # Redirect to your login view
        Except sqlite3
            return "The user or email are already registered."
            
    return render _ template ('registro.html')


HTML form (templates / registro.html):

HTML
< form method = "POST" >
    < h2 > Customer registration < / h2 >
    < label > User: < / label >
    < input type = "text" name = "user" required > < br >
    < label > Email: < / label >
    < input type = "email" name = "email" required > < br >
    < label > Password: < / label >
    < input type = "password" name = "key" required > < br >
    < button type = "submit" > Register < / button >
< / form >

3. "I forgot my password" button

Since passwords are encrypted and cannot be read, the best practice is to generate a random temporary password, update them to the database (also encrypted) and email them to the client.

To send an e-mail at Flask, we'll use the Flask-Mail library. You can install with Pip Install Flask-Mail.

Configure and Track:

Python
import rankings
import string
from flask _ mail import Mail, message

# Email server configuration (example using Gmail)
ap.config ['MAIL _ SERVER'] = 'smtp.gmail.com'
app.config ['MAIL _ PORT'] = 587
app.config ['MAIL _ USE _ TLS'] = True
app.config ['MAIL _ USERNAME'] = 'tu _ mail _ tent @ gmail.com'
ap.config ['MAIL _ PASSWORD'] = 'your _ password _ from _ application _ gmail' # Google Application Password
Email = Mail (app)

@ app.root ('/ recoup', methods = ['POST'])
def recover ():
    email = request
    
    conn = sqlite3.connect ('tienda.db')
    cur = conn.cursor ()
    cur.execute ("SELECT FROM user WHERE email users =?," (email,))
    user = cur.fetchone ()
    
    if user:
        user _ name = user [0]
        
        # 1. Generate an 8-character random time password
        temp _ key = .join (random.choices (string.ascii _ letters + string.digits, k = 8))
        temp _ key _ hash = generate _ password _ hash (temp _ key)
        
        # 2. Updating database with new time password
        cur.execute ("UPDATE users SET key =? WHERE email =?," (temp _ key _ hash, email))
        conn.commit ()
        conn.close ()
        
        # 3. Email
        Mg = Message ('Password Recovery - Stores'),
                      sender = 'tu _ mail _ tent @ gmail.com',
                      recipients = [email])
        ms.body = f "Hello {user _ name}, we have received an application to recover your password. Your new time password is: {temp _ key}\ n\ nWe recommend you change it once you login."
        
        mail.send (msg)
        That's it! We have sent you a temporary password to your email. "
    
    conn.close ()
    return "The entered mail isn't registered with the system."


Button in your login HTML (templates / login.html):

HTML
< form action = "/ recover" method = "POST" >
    < p > Have you forgotten your password? < / p >
    < input type = "email" name = "email" placeholder = "Enter your email" required >
    < button type = "submit" > Reget password < / button >
< / form >

Do you want me to show you how to set up Gmail to work with Flask-Mail?
Yes
