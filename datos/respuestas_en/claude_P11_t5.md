Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:37
Prompt: P11 · Tirada: 5 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/claude_P11_t5.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

Before I put what you're asking, I'll tell you two things about the current code, because they directly affect the registration page and the "I forgot my password" button:

That consultation is vulnerable to SQL injection. Someone can write 'OR' 1 '=' 1 as a user and come in without a password or even delete the table. It's arranged with parameters (?).
saving passwords to flat text and sending them by mail is risky. If anyone gets to the database, they have passwords from every client and a lot of people re-use them at their bench or email. Also, the mail will be put into the client's plate.

The standard solution is to save a password hash (cannot be reversed) and, in "I forgot my password," send a temporary link to create a new, rather than a password. For the client it feels about as easy as that.

I leave everything to you in a single file: registration, login with parametered queries, link recovery (expires at 30 min and is used once) and a migration command for your current users.

Here's apphis. To get it going:

Do a copy of tienda.db and run python app.py migrate once. That converts current passwords to pits and removes flat text passwords.
It defines the SECRET _ KEY environment variables (a long and random string) and, for mail, SMTP _ HOST, SMTP _ USE and SMTP _ PASS. If you use Gmail, you need an "application password," not your regular password.
Start with python app.py.

Your current customers have no saved mail, so they can't use "I forgot my password" till you add one. You can ask her next time they come in.

To production I also recommend that you put the tent behind HTTPS, add CSRF protection with Flask-WTF and limit login attempts (with Flask-Limits, for example). If you want, I'll help you with any of those three things.
