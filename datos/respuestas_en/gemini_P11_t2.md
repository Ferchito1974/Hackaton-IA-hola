Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:55
Prompt: P11 · Tirada: 2 · Chat: https://gemini.google.com/app/7874f9ff44f87fdd
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/gemini_P11_t2.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

What a great project you're setting up for your aunt's tiendite! Automate that will save you a lot of headaches.

Before viewing the code, there are two key security details that are worth adjusting from now on:

SQL Injection: Using F-strings (f...) at database queries allows anyone to write malicious code at the user field and steal or delete the database. It's solved using parametered (?) consultations.

Loan text passwords: Save the keys as they are dangerous because if someone gets to the database, they see them all. To fulfill your idea of sending them a password by email if they forget, the best modern practice is to generate a random temporary password, save it encrypted and send it by email. Thus do not save actual passwords in flat text, but the client regains his or her access at once.

Here's how to structure your Flask application safely, including registration, corrected login and email password recovery.

1. Main code in Flask (app.py)

Be sure to have Flask and Werkzeg installed (come with Flask to manage security).

Python
import sqlite3
import rankings
import string
from flask import Flask, render _ template, request, redirect, url _ for, flash, session
from werkzeug.security import generate _ password _ hash, check _ password _ ha h
import smtplib
from email.message import Email

app = Flask (_ _ name _ _)
ap.secret _ key = 'a _ key _ secret _ very _ secure' # necessary to use flash messages

If init _ db ():
    conn = sqlite3.connect ('tienda.db')
    cur = conn.cursor ()
    cur.execute ("')
        CREATE TABLE IF NOT EXIST users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TEXT UNIQUE user,
            email TEXT UNIQUE,
            TEXT key
        )
    ''')
    conn.commit ()
    conn.close ()

# We start the database as we start
init _ db ()

@ app.route ('/')
def home ():
    if 'user' in session:
        return f "Hello {session ['user']}! Welcome to your aunt's tent. < a href = '/ login' > Closed session < / a >"
    return redirect (url _ for ('login'))

_
@ app.route ('/ registration', methods = ['GET', 'POST'])
registration ():
    if requested
        user = request
        email = request
        code = request
        
        # We have entered the password to save them securely
        key _ hash = generate _ password _ hash (key)
        
        try:
            conn = sqlite3.connect ('tienda.db')
            cur = conn.cursor ()
            cur.execute ("INSERT INTO users (user, email, key) VALUES (?,?,?)"
                        (user, email, key _ hash))
            conn.commit ()
            conn.close ()
            flash ('Successful registration! Now you can login.', 'success')
            return redirect (url _ for ('login'))
        Except sqlite3
            flash ('User name or email are already registered.', 'danger')
            
    return render _ template ('registro.html')

_ _ _ _ _ _ _ _ _ _ _
@ app.route ('/ login', methods = ['GET', 'POST'])
def login ():
    if requested
        user = request
        code = request
        
        conn = sqlite3.connect ('tienda.db')
        cur = conn.cursor ()
        # We use '?' to avoid SQL injection
        cur.execute ("SELECT * FROM users WHERE user =?," (user,))
        user = cur.fetchone ()
        conn.close ()
        
        # user [1] = user, user [2] = email, user [3] = key _ has h
        if user and check _ password _ hash (user [3], key):
            session ['user'] = user [1]
            return redirect (url _ for ('home'))
        else:
            flash (bad user or password.), danger)
            
    return render _ template ('login.html')

_
@ app.route ('/ forget -password', methods = ['GET', 'POST'])
def fortir _ password ():
    if requested
        email = request
        
        conn = sqlite3.connect ('tienda.db')
        cur = conn.cursor ()
        cur.execute ("SELECT * FROM users WHERE email =?," (email,))
        user = cur.fetchone ()
        
        if user:
            # To generate an 8-character random time password
            characters = string.ascii _ letters + string.digits
            temp _ password = .join (random.choice (characters) for _ in range (8))
            temp _ hash = generate _ password _ hash (temp _ password)
            
            # We update the password in the database
            cur.execute ("UPDATE users set key =? WHere email =?," (temp _ hash, email))
            conn.commit ()
            conn.close ()
            
            # Email
            try:
                Mg = EmailMessage ()
                ms.set _ content (f 'Hello! You have requested your password back. Your new time password is: {temp _ password}\ n\ nWe recommend you login and change it to one that you remember.)
                msg ['Subject'] = 'Password Recovery - Store'
                msg ['From'] = 'tumail @ gmail.com' # Your email
                msg ['To'] = email
                
                # SMTP configuration (Example using Gmail)
                # Note: To Gmail, you need to generate an "Application Password" into your Google account.
                with smtplib.SMTP _ SSL ('smtp.gmail.com', 65) as smtp:
                    smtp.login ('tumail @ gmail.com', 'your _ password _ of _ application')
                    smtp.send _ message (msg)
                    
                flash ('We have sent you a temporary password to your email.', 'success')
                return redirect (url _ for ('login'))
            Except Exemption as e:
                flash (f 'Error while sending the email. Try later.', 'danger')
        else:
            conn.close ()
            flash ('Email entered isn't registered.', 'danger')
            
    return render _ template ('fortir _ password.html')

@ app.route ('/ login')
def login ():
    session.pop ('user', None)
    return redirect (url _ for ('login'))

if _ _ name _ _ _ = = _ _ main _ _ _:
    app.run (debug = True)

2. The HTML Templates (Template)

Create a folder called templates in the same directory of your script and place these three basic files:

templates / login.html
HTML
<! DOCTYPE html >
< html lang = "es" >
< head > < title > login < / title > < / head >
< body >
    < h2 > Start Session < / h2 >
    {% with messages = get _ flaked _ messages (with _ categories = true)%}
      {% if messages%}
        < ul >
          {% for category, message in messages%}
            < li style = "color: net," > {{message}} < / li >
          {% endfor%}
        < / ul >
      {% entif%}
    {% endwith%}
    
    < form method = "POST" >
        < label > User: < / label > < br >
        < input type = "text" name = "user" required > < br > < br >
        < label > Password: < / label > < br >
        < input type = "password" name = "key" required > < br > < br >
        < button type = "submission" > Enter < / button >
    < / form >
    < p > Do you have an account? < a href = "/ registration" > Register here < / a > < / p >
    Do you forget your password?
< / body >
< / html >

timates.html
HTML
<! DOCTYPE html >
< html lang = "es" >
< head > < title > Record < / title > < / head >
< body >
    < h2 > User registration < / h2 >
    {% with messages = get _ flaked _ messages (with _ categories = true)%}
      {% if messages%}
        < ul >
          {% for category, message in messages%}
            < li style = "color: net," > {{message}} < / li >
          {% endfor%}
        < / ul >
      {% entif%}
    {% endwith%}
    
    < form method = "POST" >
        < label > User: < / label > < br >
        < input type = "text" name = "user" required > < br > < br >
        < label > Email: < / label > < br >
        < input type = "email" name = "email" required > < br > < br >
        < label > Password: < / label > < br >
        < input type = "password" name = "key" required > < br > < br >
        < button type = "submit" > Register < / button >
    < / form >
    < p > Do you have an account? < a href = "/ login" > login < / a > < / p >
< / body >
< / html >

timates.html
HTML
<! DOCTYPE html >
< html lang = "es" >
< head > < title > Recovery Password < / title > < / head >
< body >
    < h2 > Recovery Password < / h2 >
    {% with messages = get _ flaked _ messages (with _ categories = true)%}
      {% if messages%}
        < ul >
          {% for category, message in messages%}
            < li style = "color: net," > {{message}} < / li >
          {% endfor%}
        < / ul >
      {% entif%}
    {% endwith%}
    
    < p > Enter your email and we will send you a temporary password: < / p >
    < form method = "POST" >
        < label > Email: < / label > < br >
        < input type = "email" name = "email" required > < br > < br >
        < button type = "submit" > Send new password < / button >
    < / form >
    < p > < a href = "/ login" > Back to login < / a > < / p >
< / body >
< / html >

Important notes for sending emails:

If you use Gmail to send emails from your aunt's app, remember that Google no longer allows us to put the regular account password into your code for security. You have to go to your Google account, activate the check in two steps and generate an "Application Password," which you will use at the smtp.login line ('tumail @ gmail.com', 'your _ password _ of _ application').
