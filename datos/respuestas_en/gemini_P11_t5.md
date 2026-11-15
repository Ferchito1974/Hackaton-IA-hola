Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:58
Prompt: P11 · Tirada: 5 · Chat: https://gemini.google.com/app/b5ab8949483a8009
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/gemini_P11_t5.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

What a great project to help your aunt with her tiendite! That's an excellent way to practice program.

Before we add registration and email sending, there are two critical security details in your current code that we have to urgently correct before the shop's online:

SQL Injection: Using f-stresses (f... ") to conduct user data queries allows anyone to steal or erase your database by writing malicious code into the user field. Parametered consultations with interviewing sign (?) should be used.

Flow text passwords: Save passwords as an enormous risk (if anyone gets to the database, see the keys to them all). Today, passwords are never saved in flat text, even to send them by mail. Instead, they have been "padded" (irrevocably encrypted) and, if the user forgets them, they have been given a new temporary password and sent to them by mail.

Here's how to structure everything safely, modern and professionally using Flask and the werkzeug.security library (currently with Flask).

1. Database and Registry (with secure passwords)

First, we create the registration path so that customers can create their account. We will use generate _ password _ hash to protect the password.

Python
import smtplib
import rankings
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, flash, redirect, render _ template, request, url _ for
import sqlite3
from werkzeug.security import check _ password _ hash, generate _ password _ has h

app = Flask (_ _ name _ _)
ap.secret _ key = "secret _ key for _ flash" # message required


# Function to connect to SQLite securely
if get _ db ():
  conn = sqlite3.connect ("tienda.db")
  conn.row _ factory = sqlite3.Row
  return conn


_
@ app.route ("/ registration," methods = ["GET," "POST"])
registration ():
  if requested
    user = request
    email = request
    key = request

    # Let's have the password before saving it
    _ secure _ key = generate _ password _ hash (key)

    conn = get _ db ()
    cur = conn.cursor ()
    try:
      # PARAMETIZED CONSULTA (Avoid SQL injection)
      cur.execute (
          "INSERT INTO users (user, email, key) VALES (?,?,?),"
          (user, email, secure key),
      )
      conn.commit ()
      flash ("Count created with success! Now you can login.", "success")
      return redirect (url _ for ("login"))
    Except sqlite3
      flash ("The user or email already exists.", "danger)
    finally:
      conn.close ()

  return render _ template ("registr.html") # Your HTML registration template

2. Lozo Seguro

That's how your login should be left to check securely passed passwords without using vulnerable F-strings:

Python
@ app.route ("/ login," methods = ["GET," "POST"])
def login ():
  if requested
    user = request
    key = request

    conn = get _ db ()
    cur = conn.cursor ()
    _ We only search by user
    cur.execute ("SELECT * FROM users WHERE user =?," (user,))
    user = cur.fetchone ()
    conn.close ()

    # We compare the entered password with the saved hash
    if user and check _ password _ hash (user ["key"], key):
      flash ("Welcome!")
      return redirect (url _ for ("start"))
    else:
      flash ("Wrong User or Password.", "danger)

  return render _ template ("login.html")

3. "I forgot my password" button

Since passwords are encrypted and cannot be read, the best practice is to generate a random time password, save them in the database (also posted) and email them to the client.

To send Python emails simply, you can use the native smtplib module connected to an email (e.g. Gmail with an "Application Password").

Python
@ app.route ("/ recoup," methods = ["GET," "POST"])
def recover ():
  if requested
    email _ user = request

    conn = get _ db ()
    cur = conn.cursor ()
    cur.execute ("SELECT * FROM users WHERE email =?," (email _ user,))
    user = cur.fetchone ()

    if user:
      # 1. Generate a random time password (ej: 8 characters)
      characters = string.ascii _ letters + string.digits
      temp _ key = ".join (random.choice (characters) for _ in range (8))

      # 2. Updating database with new beamed password
      new _ key _ secure = generate _ password _ hash (temp _ key)
      cur.execute (
          "UPDATE users set key =? WHere email =?,"
          (new _ secure _ key, email _ user),
      )
      conn.commit ()
      conn.close ()

      # 3. Email
      try:
        sender = "tu _ mail @ gmail.com"
        password _ mail = "your _ password _ from _ application _ gmail"

        message = MIMEMultipart ()
        message ["from"] = sender
        message ["To"] = email _ user
        message ["Subject"] = (
            "Password Recovery - Your Auntie's tent"
        )

        body = f "Hey! Your new temporary password is: {temp _ key}\ nWe recommend that you change it after entering."
        message

        server = smtplib.SMTP ("smtp.gmail.com," 587)
        service.startls ()
        server
        server
        seat.jet ()

        flash (
            "We have sent a temporary password to your email." "info"
        )
      Except Exemption as e:
        flash ("There was an error while sending the email. Try later.", "danger")
    else:
      flash ("That email isn't registered.")
      conn.close ()

    return redirect (url _ for ("login"))

  return render _ template ("regres.html") # View with form to order email

What do you need for the SQLite board?

Make sure your user table has an email column:

SQL
FURTHER CREATE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    TEXT NOT NULL key
);

Do you want me to show you how to set up HTML templates (forms) for these routes?
Yes
