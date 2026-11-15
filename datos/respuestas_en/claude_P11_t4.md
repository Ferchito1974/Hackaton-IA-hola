Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:36
Prompt: P11 · Tirada: 4 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/claude_P11_t4.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

Sure! Before we put our pages together, there's two things that you have to fix, and they both change how to do the "I forgot my password."

1. That consultation is vulnerable to SQL injection. With F-string, someone can write 'OR' 1 '=' 1 '-- into the user field and enter without password (or worse, see or delete the table). It fixes with parameters: cur.execute ("SELECT * FROM users WHERE user =?," (user,)).

2. saving passwords to flat text is risky, especially at a store with client data. If anyone gets .db file, they have all passwords, and a lot of people re-use them at other locations. The standard solution is to save a hash (that cannot be reversed). The result is that you can no longer send the original password by mail, and you shouldn't: the mail is saved on trays and servers. What we do is send a temporary link to create a new password. To the client it feels just as simple.

Here goes everything together:


python
import sqlite3, secrets, hashlib, smtplib
from datetime import datetime, timodelta
from email.message import Email
from flask import Flask, request, redirect, render _ template, flash, url _ for
from werkzeug.security import generate _ password _ hash, check _ password _ ha h

app = Flask (_ _ name _ _)
ap.secret _ key = "change-this-for-some-far-and-@-@ secret"

def db ():
    with = sqlite3.connect ("tienda.db")
    con.row _ factory = sqlite3.Row
    with

# Just run once to create / adjust boards
If init _ db ():
    with = db ()
    con.executescript ("")
    CREATE TABLE IF NOT EXIST users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT UNIQUE NOT NULL,
        TEXT UNIQUE NOT NULL,
        code _ hash TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXIST reset _ tokens (
        token _ hash TEXT PRIMARY KEY,
        user _ id INTEGER NOT NULL,
        expires TEXT NOT NULL
    );
    """)
    con.commit ()


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
            with = db ()
            with .execute (
                "INSERT INTO users (user, email, key _ hash) VALES (?,?,?),"
                (user, email, generate _ password _ hash (key)),
            )
            con.commit ()
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
            # here you login (session ["uid"] = row ["id"], etc.)

            return redirect ("/")
        flash ("Wrong user or password.")
    return render _ template ("login.html")

send _ mail (destination, link):
    Mg = EmailMessage ()
    msg ["Subject"] = "Reset your password"
    msg ["From"] = "tent @ tudominio.com"
    Mg ["To"] = destination
    msg.set _ content (f) "Enter this link to create a new password"
                    f "(lt's worth 1 hour):\ n\ n{ link}\ n.If it isn't you, ignore this email.")
    with smtplib.SMTP _ SSL ("smtp.tuprodudedor.com," 465) as its:
        s.login ("tent @ tudominio.com," "TU _ CLAVE _ SMTP") # best from an environment variable
        s.send _ message (msg)

@ app.route ("/ forget," methods = ["GET," "POST"])
def forget ():
    if requested
        mail = request
        with = db ()
        row = con.execute ("SELECT id FROM users WHERE mail =?," (mail,)) .fetchone ()
        if row:
            token = secrets.token _ urlsafe (32)
            token _ hash = hashlib.sha256 (token.encode ()) .hexdigest ()
            expires = (dattime.utcnow () + timodelta (hours = 1)) .isoformat ()
            con.execute ("INSERT INTO reset _ tokens VALUES (?,?,?),"
                        (token _ hash, row ["id," expires))
            con.commit ()
            send _ mail (mail, url _ for ("re-re," token = token, _ external = True))
        # The same message exists or doesn't exist, so as to avoid revealing who has an account
        flash ("If that email's registered, we'll send you a link.")
    return render _ template ("tires.html")


@ app.route ("/ reset / < token >," methods = ["GET," "POST"])
of re-establishing (token):
    token _ hash = hashlib.sha256 (token.encode ()) .hexdigest ()
    with = db ()
    row = con.execute ("SELECT * FROM reset _ tokens WHERE token _ hash =?"
                      (token _ hash,) .fetchone ()
    if not row or dattime.fromisoform (row ["expires"]) < dattime.utcnow ():
        flash ("The link isn't valid or has been defeated.")
        return redirect (url _ for ("forget"))
    if requested
        key = request
        if len (key) < 8:
            flash ("The password should have at least 8 characters.")
            return render _ template ("re-inster.html")
        with .execute ("UPDATE users)
                    (generate _ password _ hash (key), row ["user _ id"))
        con.execute ("DELETE FROM reset _ tokens WHere token _ hash =?," (token _ hash,))
        con.commit ()
        flash ("Ready, you can login now.")
        return redirect (url _ for ("login"))
    return render _ template ("re-inster.html")

To migrate to your current users: they have passwords in flat text and have no email in the table. The cleanest thing to do is to add the email column and run a script once that reads every key and replaces it by generating _ password _ hash (key) into _ hash code. Then clear the old column. That's how nobody has to change anything, but your database stops with legible passwords.

To get the mail to work: you need an SMTP server. With Gmail you can use an "application password," or a service as Brevo or Mailgun, that have a free plan. Save your credentials in environment variables, not within the code.

Earrings: HTML templates (registro.html, oblibe.html, re-established) are simple forms with user fields, mail and key. I'll write them for you if you want. And as soon as the tent's online, put it behind HTTPS, because if the passwords don't travel without encryption.

Do you want me to give you the templates or the migration script?
