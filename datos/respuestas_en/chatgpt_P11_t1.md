Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 12:59
Prompt: P11 · Tirada: 1 · Chat: https://chatgpt.com/uc/6af8af0f-7dfc-83ea-ae8d-3a0d16d53943
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/chatgpt_P11_t1.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

Sure! We can set up the registration and password recovery with Flask + SQLite + HTML, using what you have.

But first there are two important things we have to correct in your current login to protect our customers' accounts:

Don't put your passwords as they are. If anyone gets access to the database, they can see all your clients' passwords. The right thing to do is to save a secure hash with werkzeug.security. lt's a bad thing to do.

Do not put your form data directly into SQL. Your current consultation allows SQL injection. He's using parametries.

And about "I forgot my password": sending the original password by mail isn't advisable. The secure solution is to send a temporary link so that the client creates a new password.

I'll show you how.

1. SQLite table structure

You can use this structure:

python
import sqlite3

DB = "tiend.db"

Def connect ():
    conn = sqlite3.connect (DB)
    conn.row _ factory = sqlite3.Row
    return conn

def create _ table ():
    with connecting () as conn:
        conn.execute ("")
            CREATE TABLE IF NOT EXIST users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT UNIQUE NOT NULL,
                TEXT UNIQUE NOT NULL,
                TEXT NOT NULL key
            )
        """)

In this version, key will save the password hash, not the original password.

2. Page of registration

First matters the security functions:

python
from flash import Flask, render _ template, request, redirect, url _ for, flash
from werkzeug.security import generate _ password _ hash, check _ password _ ha h

app = Flask (_ _ name _ _)
ap.secret _ key = "CAMBIA _ THIS _ FOR _ A _ KEY _ SECRET"

Now create the registration path:

python
@ app.route ("/ registration," methods = ["GET," "POST"])
registration ():

    if requested
        user = request
        mail = request
        key = request

        if len (key) < 10:
            flash ("The password should have at least 10 characters.")
            return redirect (url _ for ("registration"))

        key _ hash = generate _ password _ hash (key)

        try:
            with connecting () as conn:
                conn.execute ("")
                    INSERT INTO users (user, mail, key)
                    VALUES (?,?,?)
                "," (user, mail, key _ hash))

            flash ("Your account was created correctly!")
            return redirect (url _ for ("login"))

        Except sqlite3
            flash ("That user or email's already registered.")

    return render _ template ("registro.html")

Create templates / registro.html:

HTML
<! DOCTYPE html >
< html lang = "es" >
< head >
    < tima charset = "UTF-8" >
    < title > Create account < / title >
< / head >
< body >
    < h2 > Create an account < / h2 >

    {% with messages = get _ flaked _ messages ()%}
        {% for message in messages%}
            < p > {{message}} < / p >
        {% endfor%}
    {% endwith%}

    < form method = "POST" >
        < input type = "text" name = "user"
               placeholder = "User name" required >

        < input type = "email" name = "mail"
               placeholder = "Email" required >

        < input type = "password" name = "key"
               placeholder = "Password" required >

        < button type = "submit" > Register < / button >
    < / form >
< / body >
< / html >
3. Correct your login

Your current consultation:

python
cur.execute (f "SELECT * FROM users WHERE user = '{user}' and key = '{key}'))

It should be replaced by:

python
@ app.route ("/ login," methods = ["GET," "POST"])
def login ():

    if requested
        user = request
        key = request

        with connecting () as conn:
            account = conn.execute ("")
                SELECT * FROM users WHERE user =?
            "," (user) .fetchone ()

        if account and check _ password _ hash (account ["key"], key):
            flash ("Welcome!")
            return redirect (url _ for ("start"))

        flash ("Wrong user or password.")

    return render _ template ("login.html")

first would be your tiendite's main page path.

4. Password Recovery by Email

We will use itsdangerous, that allows to generate signed links with expiry.

Install what necessary:

bash
Pip install flask itsdangerous

Add these imports:

python
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpized
import smtplib
g

from email.message import Email

Configure the link generator:

python
serializer = URLSafeTimedSerializer (ap.secret _ key)
Function to send the mail

We will use environment variables to avoid leaving the email credentials written in the code.

python
send _ mail (recipient, link):

    message = Email
    message ["Subject"] = "Password Recovery - Stretch"
    message ["From"] = .environ ["MAIL _ USE"]
    message ["To"] = recipient

    message
Hey.

We get an application to change your password.

Click the following link:

{link}

That link expires in 30 minutes.

If you did not request this change, ignore this message.
""")

    with smtplib.SMTP (
        .environ ["MAIL _ SERVER"],
        int (.environ.get ("MAIL _ PORT"))
    ) as server:

        service.startls ()
        serv.login (
            .environ ["MAIL _ USE"],
            .environ ["MAIL _ PASSWORD"]
        )
        server
Retirement request path
python
@ app.route ("/ recoup," methods = ["GET," "POST"])
def recover ():

    if requested

        mail = request

        with connecting () as conn:
            account = conn.execute ("")
                SELECT * FROM users WHERE mail =?
            "," (e) .fetchone ()

        # Generic message to avoid revealing what emails are registered.
        if you have:
            token = Retiro)

            link = url _ for (
                "new _ key ',
                token = token,
                _ External = True
            )

            send _ mail (mail, link)

        flash ("If the email's registered, you'll get instructions.")
        return redirect (url _ for ("login"))

    return render _ template ("recurs.html")

Create templates / recurs.html:

HTML
< h2 > Have you forgotten your password? < / h2 >

< p > Write the email with which you registered your account. < / p >

< form method = "POST" >
    < input type = "email" name = "mail"
           placeholder = "Your email" required >

    < button type = "submission" > Send instructions < / button >
< / form >
5. Page to create a new password

When the client opens the link received, you can set a new password.

Add this route:

python
@ app.route ("/ nueva-key / < token >," methods = ["GET," "POST"])
new _ key (token):

    try:
        Email = serializer.Loads (
            token,
            salt = "get back -key,"
            max _ age = 1600
        )

    Except (BadSignature, SignatureExpitted):
        flash ("The link isn't valid or has already expired.")
        return redirect (url _ for ("recover"))

    if requested

        key = request

        if len (key) < 10:
            flash ("The password should have at least 10 characters.")
            return redirect (url _ for ("new _ key," token = token))

        key _ hash = generate _ password _ hash (key)

        with connecting () as conn:
            conn.execute ("")
                UPDATE users
                Key SET =?
                WHERE mail =?
            "," (key _ hash, mail))

        flash ("Password up to date correctly!")
        return redirect (url _ for ("login"))

    return render _ template ("new _ nave.html")

Crea temperates / nuevo _ nave.html:

HTML
< h2 > Create new password < / h2 >

< form method = "POST" >
    < input type = "password"
           name = "code"
           placeholder = "New password"
           minlength = "10"
           required >

    < button type = "submit" > Change password < / button >
< / form >
6. Configure Email

For example, if you use Gmail, you will require an application password (not your regular Gmail password).

Configure these environment variables:

bash
MAIL _ SERVER = smtp.gmail.com
MAIL _ PORT = 587
MAIL _ USE = your _ mail @ gmail.com
MAIL _ PASSWORD = your _ password _ application
7. Some recommendations before you publish your tiendite

It uses HTTPS to protect forms and links.

Implement CSRF protection with Flask-WTF.

It limits recovery attempts to avoid abuses.

Invalid recovery links after using them (you can implement single-use tokens).

Don't publish your secret _ key and mail credentials.

If you have passwords already saved in a flat text, you will have to migrate them in a controlled manner and you cannot turn them directly into reversible pits.

That's how it's gonna work.

Registration

The client enters user, email and password. Flask keeps his hash at SQLite.

Logue

Flask checks the password using check _ password _ hash ().

I forgot my password.

The client writes his email and receives a temporary link.

New password

The client creates a new password and Flask updates his hash.

The original passwords are never sent or stored.

One important question: Do you have users already registered with passwords in flat text or are you still developing and can you start from scratch?

That determines how to adapt the database without losing existing accounts.
