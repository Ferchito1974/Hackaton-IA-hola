Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:08
Prompt: P11 · Tirada: 5 · Chat: https://chatgpt.com/uc/6af8b134-42c4-83ea-bf61-77e85572f651
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/chatgpt_P11_t5.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

Of course! Can we put together the registration and password recovery for your tiendite using Python + Flask + SQLite, without complicating the project.

But first there are two important things we have to correct in your current login:

Your SQL consultation is vulnerable to SQL injection. By directly inserting user and key into the text of the query, someone could manipulate them.

Don't put passwords as they are. Even if you wish to send them to your client once they have been forgotten, saving them to a flat text puts at risk all accounts if someone gets to the database.

The solution is to save passwords by means of a secure hash and, as someone forgets them, allow them to set up a new one with a link sent to their email. That way you don't have to know or send his earlier password.

1. Correct your login

Flask already has tools to protect passwords with werkzeug.security.

python
from werkzeug.security import generate _ password _ hash, check _ password _ ha h

♪ At login
cur.execute (
    "SELECT * FROM users WHERE user =?,"
    (user)
)

user = cur.fetchone ()

if user and check _ password _ hash (user ["key"], key):
    print ("Correct login")
else:
    print ("Wrong user or password")

That means your SQLite connection uses sqlite3.Row to gain access to columns by name.

2. Prepare user table

We need to add an email and two fields to get your password back.

If you will create a new table:

sql
FURTHER CREATE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    TEXT NOT NULL key,
    token _ recovery TEXT,
    Expiration _ token TEXT
);

If you have the table created, you can add the columns without deleting your users:

sql
ALTER TABLES ADD COLUMN email TEXT users
ALTER TABLO users ADD COLUMN token _ retrieval TEXT
ALTER TABLES ADD COLUMN users expires _ TOken TEXT;

Important: If you already have passwords saved in flat text, you will have to convert them to pits by means of a migration before using the new login. Do a backup of SQLite first.

3. Create registration page

In your file app.py:

python
from flash import Flask, render _ template, request, redirect, url _ for, flash
import sqlite3

from werkzeug.security import generate _ password _ has h

app = Flask (_ _ name _ _)
ap.secret _ key = "CAMBIA _ THIS _ BY _ A _ SECRET _ ALEATORIO"

Def connect ():
    conn = sqlite3.connect ("tiend.db")
    conn.row _ factory = sqlite3.Row
    return conn

@ app.route ("/ registration," methods = ["GET," "POST"])
registration ():

    if requested

        user = request
        email = request
        key = request

        if no user or no email or no key:
            flash ("Complete all fields.")
            return redirect (url _ for ("registration"))

        key _ hash = generate _ password _ hash (key)

        try:
            conn = connect ()
            cur = conn.cursor ()

            cur.execute ("")
                INSERT INTO users (user, email, key)
                VALUES (?,?,?)
            "," (user, email, key _ hash))

            conn.commit ()
            conn.close ()

            flash ("Successful registration!")
            return redirect (url _ for ("login"))

        Except sqlite3
            flash ("That user or email's already registered.")

    return render _ template ("registro.html")

And create templates / registro.html:

HTML
< h2 > Create account < / h2 >

< form method = "POST" >

    < label > User: < / label >
    < input type = "text" name = "user" required >

    < label > Email: < / label >
    < input type = "email" name = "email" required >

    < label > Password: < / label >
    < input type = "password" name = "key" required >

    < button type = "submit" > Register < / button >

< / form >
4. To create "I forgot my password"

The idea will be as follows:

The client writes his email

On the recovery page.

Flask generates a random token

He keeps it temporarily and sends a link to his mail.

The client opens the link

The token's valid for about 15 minutes.

The client creates a new password

He keeps his hash and invalids his token.

Code to generate and send the mail

We'll use secrets to create a secure and smtplib token to send the email.

Add these imports:

python
import secrets
import hashlib
g
import smtplib

from datetime import datetime, timedelta, timezone
from email.message import Email

Configure sending mail using environment variables:

python
SMTP _ SERVER = "smtp.gmail.com"
SMTP _ PORT = 587

EMAIL _ USE = .environ ["EMAIL _ USE"]
EMAIL _ PASSWORD = .environ ["EMAIL _ PASSWORD"]

Do not put the Gmail password directly into the code. If you use Gmail, you can set an application password.

Function to send the email:

python
send _ mail (recipient, link):

    message = Email
    message ["Subject"] = "Recover password - Stretch"
    message ["From"] = EMAIL _ USE
    message ["To"] = recipient

    message
Hey.

We get an application to change your password.

Click this link to create a new password:

{link}

That link expires in 15 minutes.

If you haven't requested this change, ignore this email.
""")

    with smtplib.SMTP (SMTP _ SERVER, SMTP _ PORT) as server:
        service.startls ()
        seapor.login (EMAIL _ USE, EMAIL _ PASSWORD)
        server
Track to demand recovery
python
@ app.route ("/ recoup," methods = ["GET," "POST"])
def recover ():

    if requested

        email = request

        conn = connect ()
        cur = conn.cursor ()

        cur.execute (
            "SELECT id FROM users WHERE email =?,"
            (email,)
        )

        user = cur.fetchone ()

        if user:
            token = secrets.token _ urlsafe (32)

            token _ hash = hashlib.sha256 (
                token.encode ()
            ) .hexdigest ()

            Expiration = (
                datetyme.now (timezone.utc)
                + timidelta (minutes = 15)
            ) .isoformat ()

            cur.execute ("")
                UPDATE users
                SET token _ recovery =?,
                    Expiration _ token =?
                WHERE id =?
            "," (token _ hash, expiry, user ["id"))

            conn.commit ()

            link = url _ for (
                "new _ key ',
                token = token,
                _ External = True
            )

            send _ email (email, link)

        conn.close ()

        flash (
            "If the email's registered, you'll get instructions to get your account back."
        )

        return redirect (url _ for ("recover"))

    return render _ template ("recurs.html")

Create templates / recurs.html:

HTML
< h2 > Reget password < / h2 >

< form method = "POST" >

    < label > Email: < / label >

    < input
        type = "email"
        name = "email"
        required
    >

    < button type = "submission" >
        Send Link
    < / button >

< / form >
5. Page to set a new password

That's a valid token path, check that you haven't won and update your password.

python
from werkzeug.security import generate _ password _ has h

@ app.route ("/ nueva-key / < token >," methods = ["GET," "POST"])
new _ key (token):

    token _ hash = hashlib.sha256 (
        token.encode ()
    ) .hexdigest ()

    conn = connect ()
    cur = conn.cursor ()

    cur.execute ("")
        SELECT id, expiration _ token
        FROM users
        WHERE TOken _ Recovery =?
    "," (token _ hash,))

    user = cur.fetchone ()

    if not user:
        conn.close ()
        return "Invalid or already used link."

    Expiration = datetime.fromisoformat (
        user ["expiry _ token"]
    )

    if dattime.now (timezone.utc) > expiry:
        conn.close ()
        "The link has expired. Request a new one."

    if requested

        key = request

        if len (key) < 10:
            conn.close ()
            return "The password should have at least 10 characters."

        key _ hash = generate _ password _ hash (key)

        cur.execute ("")
            UPDATE users
            Key SET =?,
                token _ recovery = NULL,
                expiration _ token = NULL
            WHERE id =?
        "," (key _ hash, user ["id"))

        conn.commit ()
        conn.close ()

        return redirect (url _ for ("login"))

    conn.close ()

    return render _ template ("new _ nave.html")

Crea temperates / nuevo _ nave.html:

HTML
< h2 > Create new password < / h2 >

< form method = "POST" >

    < label > New password: < / label >

    < input
        type = "password"
        name = "code"
        minlength = "10"
        required
    >

    < button type = "submission" >
        Change Password
    < / button >

< / form >
6. Add the button to login

At your templates / login.html add:

HTML
< a href = "{{url _ for ('registration')}" >
    Creating an account
< / a >

< br >

< a href = "{{url _ for ('recover')}" >
    Have you forgotten your password?
< / a >
7. Final project structure

Your project could be as follows:

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
    Reg.
8. Some recommendations before put them online

It uses HTTPS to protect data that are sent between the browser and Flask.

It implements CSRF protection, for example with Flask-WTF.

It limits login attempts and recovery requests.

Don't reveal if an email's registered or not.

Save SMTP and SECRET _ KEY credentials to environment variables.

Configure an HTTPS public URL to generate recovery links.

Do not allow them to re-use or use tokens after their expiry.

My recommendation: Don't put passwords back into flat text. Even the person with the tiendite doesn't have to know them. If a client forgets them, they can always create a new one.

A question about your project

Do your user table currently have only id, user and key columns, or do you have an email column as well?

If you share with me the current structure of your table and your complete login code (with no real passwords), I can adapt all this to your project without you have to start from scratch.
