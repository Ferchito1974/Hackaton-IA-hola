Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:25
Prompt: P10 · Tirada: 2 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/claude_P10_t2.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

To get your Flask project up to GitHub

Before you do anything: your .env has your OpenAI key API and database password. In a public repo, bots constantly scour GitHub and steal keys in minutes. That's why the first step is to create a .gitignore, before the first git add.

1. Commands

From the project folder:


bash
git init

To ignore unnecessary secrets and archives
Cat > .gitignore < < 'EOF'
.env
_ _ pycache _ _ /
* .pyc
venv /
.venv /
instance /
.db
* .sqlite3
. DS _ Store
.vscode /
EOF

# Variables with no real values (this does rise)
cat > .env.example < < 'EOF'
OPENAI _ API _ KEY = your _ api _ key _ here
DB _ PASSWORD = your _ password _ here
EOF

He verifies that .env was excluded:


bash
git status

.env should NOT appear on the list. If she shows up, stop and check the .gitignor.


bash
git add.
git commit -m "First commit: app Flask"
git branch -M main
2. Create Rep at GitHub

Enter Github.com → New repository → name him, public mark and do not mark "Add to Readme" (you have one). Then copies the URL and runs:


bash
git remote add origin https: / / github.com / TU _ USUARIO / TU _ REPO.git
git push -u origin main

(If you use GitHub CLI, it's a single command: gh repo create nombre-repo --public --source =. --push)

3. Check your code

Make sure that app.py reads the secrets of the environment and doesn't have them written directly:


python
g
from dotenv import load _ dotenv

load _ dotenv ()
api _ key = .environ ["OPENAI _ API _ KEY"]

Check your code if there's a password or handwritten key. If there is, move her to .env before the commit. Also, add python-dotenv to your required.

If at some point you have uploaded .env (even if you have deleted it later): revoks the key API into the OpenAI Panel and changes the database password. Git's record keeps everything.

4. Readme template

Replace what's in square brackets. A capture or GIF of the app makes a great difference for whoever checks your CV.


markdown
Project Name

Description in one or two phrases: what the app does and what problem resolves.

[App capture] (static / screenshot.png)

# # Characteristics

- Main feature 1
- Main characteristic 2
- Integration with OpenAI API for [what does]

technologies

- Python 3 / Flask
- OpenAI API
- [Database: PostgreSQL / SQLite / MySQL]
- HTML, CSS, Jinja2

Installation

1. Clone the repository:
   "'bas h
   git clone https: / / github.com / TU _ USUARIO / TU _ REPO.git
   cd TU _ REPO
   ```

2. It creates and activates a virtual environment:
   "'bas h
   python -m venv venv
   source venv / bin / activate # On Windows: venv\ Scripts\ activate
   ```


3. Install the units:
   "'bas h
   Pip install -r require
   ```

4. Configure the environment variables:
   "'bas h
   cp .env.example .env
   ```
   Edit .env with your OpenAI key API and database password.

5. Run the app:
   "'bas h
   flask run
   ```
   Open http: / / 127.0.0.1: 5,000 in your browser.

Project structure

```
Reg.
Retirement
″ ″ static / # CSS, JS and images
Reg.
Reg.
```

♪ ♪ What I learned

A short paragraph about challenges you faced and what you learned. The recruiters are interested in this.


Author

* * Your Name * * · [LinkedIn] (https: / / Linkedin.com / in / tu-profile)

To update the README after: edit it, and then git add README.md, git commit -m "Add README" and git push.

If you wish, hit me with your ap.py (without the keys) and check that there are no handwritten secrets or bad practices an recruiter can notice.
