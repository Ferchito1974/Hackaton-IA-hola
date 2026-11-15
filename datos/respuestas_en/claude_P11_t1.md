Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:30
Prompt: P11 · Tirada: 1 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/claude_P11_t1.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

I'll help you with both, but first two changes to what you have already, because they're the ones that can afford your aunt most:

F-string in SQL allows SQL injection. If anyone writes' OR '1' = '1' -- as a user, they enter without a password (even as an administrator). It's arranged with parameters (?).
saving passwords into flat text means that, if someone gets to copies the database, they have passwords from all your customers, and many re-use them in their mail or bench. That's why they're saved with hash, and that's why you can't send the password by mail: it doesn't exist to get them back. The standard is to send a temporary link to select a new one. It's as comfortable for him and far safer.
Installation

bash
Pip install flask

(werkzeung and itsdangerous have come with Flask.)

Code

python
g
import sqlite3
import smtplib
from email.message import Email
from flask import Flask, request, redirect, render _ template, session, url _ for, flash
from werkzeug.security import generate _ password _ hash, check _ password _ ha h
from itsdangerous import URLSafeTimedSerializer, SignatureExpied, BadSignature

app = Flask (_ _ name _ _)
ap.secret _ key = .environ ["SECRET _ KEY"] # a long and random string, out of code
serializer = URLSafeTimedSerializer (ap.secret _ key)

def db ():
    with = sqlite3.connect ("tienda.db")
    con.row _ factory = sqlite3.Row
    with

# Table (add the email column if you have)
_
# id INTEGER PRIMARY KEY,
# user TEXT UNIQUE NOT NULL,
# email TEXT UNIQUE NOT NULL,
# key _ hash TEXT NOT NULL
# );

@ app.route ("/ registration," methods = ["GET," "POST"])
registration ():
    if requested
        user = request
        mail = request
        key = request
        if len (key) < 8:

            flash ("The password should have at least 8 characters.")
            return render _ template ("registro.html")
        try:
            with db () as with:
                with .execute (
                    "INSERT INTO users (user, email, key _ hash) VALES (?,?,?),"
                    (user, email, generate _ password _ hash (key)),
                )
        Except sqlite3
            flash ("That user or email's already registered.")
            return render _ template ("registro.html")
        return redirect (url _ for ("login"))
    return render _ template ("registro.html")

@ app.route ("/ login," methods = ["GET," "POST"])
def login ():
    if requested
        user = request
        key = request
        row = db () .execute (
            "SELECT * FROM users WHERE user =?," (user,)
        ) .fetchone ()
        if row and check _ password _ hash (row ["key _ hash"], key):
            session ["user _ id"] = row ["id"]
            return redirect (url _ for ("start"))
        flash ("Wrong user or password.")
    return render _ template ("login.html")

send _ mail (destination, link):
    Mg = EmailMessage ()
    msg ["Subject"] = "Reforms your password"
    Mg ["From"] = .environ ["SMTP _ USE"]

    Mg ["To"] = destination
    msg.set _ content (
        f "Enter this link to choose a new password"
        f "(expires in 1 hour):\ N {link}\ N {link}
        f "If it isn't you, ignore this message."
    )
    with smtplib.SMTP _ SSL ("smtp.gmail.com," 465) as its:
        .login (.environ ["SMTP _ USE"], .environ ["SMTP _ pASS"])
        s.send _ message (msg)

@ app.route ("/ forget," methods = ["GET," "POST"])
def forget ():
    if requested
        mail = request
        row = db () .execute (
            "SELECT id, key _ hash FROM users WHERE mail =?," (mail,)
        ) .fetchone ()
        if row:
            # Include some of the hash makes the link stop serving once used
            token = serializer
                {"id": row ["id"], "h": row ["key _ hash"] [-10:], salt = "reset"
            )
            link = url _ for ("re-establish," token = token, _ external = True)
            send _ mail (mail, link)
        # The same message exists or doesn't exist, so as to avoid revealing who has an account
        flash ("If the email's registered, we send you a link.")
        return redirect (url _ for ("login"))
    return render _ template ("tires.html")

@ app.route ("/ reset / < token >," methods = ["GET," "POST"])
of re-establishing (token):
    try:

        data = serializer.Loads (token, salt = "reset," max _ age = 3600)
    Except (SignatureExpized, BadSignature):
        flash ("The link isn't valid or has been defeated.")
        return redirect (url _ for ("forget"))

    with = db ()
    row = con.execute ("SELECT id, key _ hash FROM users WHERE id =?") .fetchone ()
    if not row or row ["key _ hash"] [-10:]! = data ["h"]:
        flash ("That link was already used.")
        return redirect (url _ for ("forget"))

    if requested
        new = request
        if len (new) < 8:
            flash ("The password should have at least 8 characters.")
            return render _ template ("re-inster.html")
        with:
            with .execute (
                "UPDATE users
                (generate _ password _ hash (new), row ["id"]),
            )
        flash ("Password up to date. Now you can come in.")
        return redirect (url _ for ("login"))
    return render _ template ("re-inster.html")
Migrate to users you already have

Run this once to convert current passwords to hash (and then erase old column):


python
with = sqlite3.connect ("tienda.db")
con.execute ("ALTER TABLE users ADD COLUMN key _ hash TEXT")
for id _, key in con.execute ("SELECT id, key FROM users") .fetchall ():
    with .execute ("UPDATE users)
                (generate _ password _ hash (key), id _))
con.commit ()
# When you check that everything works: ALTER TABLE users DROP COLUMN key
Practical note
Email: with Gmail you need an "application password" (by activates a two-step check), not a regular password. Save SMTP _ USER, SMTP _ PASS and SECRET _ KEY in environment variables, not code.
Stages: registro.html, login.html, oblibe.html and re-established are simple forms with method = "post." If you want, I'll write them to you.
Before you publish it: use HTTPS and consider adding CSRF (Flask-WTF) protection and limiting login attempts (Flask-Limited).

Do you want me to give you HTML templates as well?
