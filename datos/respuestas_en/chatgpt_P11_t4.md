Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:06
Prompt: P11 · Tirada: 4 · Chat: https://chatgpt.com/uc/6af8b0bc-bc70-83ea-b7ca-eb5c51b62e3f
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/chatgpt_P11_t4.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

Of course! Can we put up the registration and password recovery with Flask + SQLite + Python, using what you have.

But first there are two important details of your current code that should be rectified so that tiendite doesn't become vulnerable:

Your SQL consultation is vulnerable to SQL injection. By directly inserting user and key into SQL, someone could manipulate the form to alter the query.

Don't save passwords in flat text. Even if you wish to send them to your customers after they have been forgotten, it's safer to save a hash. If you miss your password, you can create a new password using a link sent to your email.

I propose to use werkzeug.security, that's coming with Flask, and temporary recovery tokens.

1. Prepare database

Your user table can have this structure:

python
import sqlite3

Def connect ():
    conn = sqlite3.connect ("tiend.db")
    conn.row _ factory = sqlite3.Row
    return conn

def create _ table ():
    conn = connect ()
    conn.execute ("")
        CREATE TABLE IF NOT EXIST users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT UNIQUE NOT NULL,
            TEXT UNIQUE NOT NULL,
            TEXT NOT NULL key
        )
    """)
    conn.commit ()
    conn.close ()

The key column will now save the password's hash, and not the original password.

2. Page of registration

Install Flask if you haven't got it:

bash
Pip install flask

In your file app.py:

python
from flash import Flask, render _ template, request, redirect, url _ for, flash
from werkzeug.security import generate _ password _ hash, check _ password _ ha h
import sqlite3

app = Flask (_ _ name _ _)
ap.secret _ key = "CAMBIA _ THIS _ BY _ A _ SECRET _ ALEATORIO"

create _ table ()

@ app.route ("/ registration," methods = ["GET," "POST"])
registration ():
    if requested
        user = request
        mail = request
        key = request

        if no user or no email or len (key) < 8:
            flash ("Complete data. The password should have at least 8 characters.")
            return redirect (url _ for ("registration"))

        key _ hash = generate _ password _ hash (key)

        conn = connect ()

        try:
            conn.execute (
                "INSERT INTO users (user, mail, key) VALES (?,?,?),"
                (user, email, key _ hash)
            )
            conn.commit ()
            flash ("Account created correctly!")
            return redirect (url _ for ("login"))

        Except sqlite3
            flash ("That user or email's already registered.")

        finally:
            conn.close ()

    return render _ template ("registro.html")

Create templates / registro.html:

HTML
<! DOCTYPE html >
< html lang = "es" >
< head >
    < tima charset = "UTF-8" >
    < title > Record - My tent < / title >
< / head >
< body >
    < h2 > Create an account < / h2 >

    {% with messages = get _ flaked _ messages ()%}
        {% for message in messages%}
            < p > {{message}} < / p >
        {% endfor%}
    {% endwith%}

    < form method = "POST" >
        < label > User: < / label >
        < input type = "text" name = "user" required >

        < br > < br >

        < label > Email: < / label >
        < input type = "email" name = "mail" required >

        < br > < br >

        < label > Password: < / label >
        < input type = "password" name = "key" minlength = "8" required >

        < br > < br >

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

        conn = connect ()

        account = conn.execute (
            "SELECT * FROM users WHERE user =?,"
            (user)
        ) .fetchone ()

        conn.close ()

        if account and check _ password _ hash (account ["key"], key):
            flash ("Welcome!")
            return redirect (url _ for ("start"))

        flash ("Wrong user or password.")

    return render _ template ("login.html")

first would be your tiendite's main page path.

4. Recovery Password by Email

Here's what's interesting: Instead of sending the forgotten password, we will send a link that will create a new one.

We'll use itsdangerous, that's usually already installed with Flask.

Add to app.py:

python
from itsdangerous import URLSafeTimedSerializer, SignatureExpied, BadSignature
from flask import url _ for
g
import smtplib
from email.message import Email

serializer = URLSafeTimedSerializer (ap.secret _ key)

send _ mail (recipient, link):
    message = Email
    message ["Subject"] = "To recover password - My tent"
    message ["From"] = .environ ["EMAIL _ USE"]
    message ["To"] = recipient

    message
Hey:

We have an application to restore your password.

Click the following link:

{link}

That link expires in 15 minutes.

If you didn't demand this change, ignore this email.
""")

    with smtplib.SMTP _ SSL ("smtp.gmail.com") as server:
        serv.login (
            .environ ["EMAIL _ USE"],
            .environ ["EMAIL _ PASSWORD"]
        )
        server
Retirement request path
python
@ app.route ("/ oblivion," methods = ["GET," "POST"])
Of oblivion ():
    if requested
        mail = request

        conn = connect ()
        account = conn.execute (
            "SELECT * FROM users WHERE mail =?,"
            (mail)
        ) .fetchone ()
        conn.close ()

        if you have:
            token = Retiro)

            link = url _ for (
                "re-establishing,"
                token = token,
                _ External = True
            )

            send _ mail (mail, link)

        flash ("If the email is registered, you will be instructed to get your account back.")
        return redirect (url _ for ("oblivion"))

    return render _ template ("notio.html")

Create template / timo.html:

HTML
<! DOCTYPE html >
< html lang = "es" >
< head >
    < tima charset = "UTF-8" >
    < title > I forgot my password < / title >
< / head >
< body >
    < h2 > Reget password < / h2 >

    {% with messages = get _ flaked _ messages ()%}
        {% for message in messages%}
            < p > {{message}} < / p >
        {% endfor%}
    {% endwith%}

    < form method = "POST" >
        < label > Email: < / label >
        < input type = "email" name = "mail" required >

        < button type = "submission" > Send instructions < / button >
    < / form >
< / body >
< / html >
5. Page to set new password

When the client opens the email link, you can choose a new password.

Add this route:

python
@ app.route ("/ reset / < token >," methods = ["GET," "POST"])
of re-establishing (token):

    try:
        Email = serializer.Loads (
            token,
            salt = "get back -key,"
            max _ age = 900 # 15 minutes
        )
    Except (SignatureExpized, BadSignature):
        flash ("The link expired or isn't valid.")
        return redirect (url _ for ("oblivion"))

    if requested
        key = request

        if len (key) < 8:
            flash ("The password should have at least 8 characters.")
            return redirect (url _ for ("re-establish," token = token))

        key _ hash = generate _ password _ hash (key)

        conn = connect ()
        conn.execute (
            "UPDATE users
            (key _ hash, mail)
        )
        conn.commit ()
        conn.close ()

        flash ("Your password was updated!")
        return redirect (url _ for ("login"))

    return render _ template ("re-inster.html")

Create templates / re-established

HTML
<! DOCTYPE html >
< html lang = "es" >
< head >
    < tima charset = "UTF-8" >
    < title > New < / title >
< / head >
< body >
    < h2 > Create new password < / h2 >

    {% with messages = get _ flaked _ messages ()%}
        {% for message in messages%}
            < p > {{message}} < / p >
        {% endfor%}
    {% endwith%}

    < form method = "POST" >
        < label > New password: < / label >
        < input type = "password" name = "key"
               minlength = "8" required >

        < button type = "submission" > Save password < / button >
    < / form >
< / body >
< / html >
6. Configure Email

If you use Gmail:

It activates monitoring in two steps.

Generates an application password into your Google account.

Configure these environment variables on your server:

bash
EMAIL _ USE = your _ mail @ gmail.com
EMAIL _ PASSWORD = your _ password _ application

Do not put Gmail's password directly into your code.

7. What the project would look like
text
tidite /
│
Hey.
Reg.
│
Reg.
    Reg.
    Reg.
    Reg.
    Reestablishment

At your login, add your access to registration and recovery:

HTML
< a href = "{{url _ for ('registration')}" >
    Create Account
< / a >

< br >

{{url _ for ('oblivion')}} >
    Have you forgotten your password?
< / a >
8. 3 recommendations before put them online

If you have users with passwords with a flat text, you will need to migrate their passwords to the new system and do not simply change login consultation.

Add CSRF protection with Flask-WTF and login and Recovery Test Limits.

Recovery tokens should be single-use. To do so, you should save your identifier or status at SQLite and mark them as used after the change.

One important question to continue: Do your tiendite have users registered with SQLite with passwords saved as, or are you barely starting?

I'm asking because I can help you make the transition without your aunt losing the customers she's already registered with.
