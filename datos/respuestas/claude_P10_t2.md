Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:25
Prompt: P10 · Tirada: 2 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Subir tu proyecto Flask a GitHub

Antes de hacer nada: tu .env tiene tu API key de OpenAI y la contraseña de la base de datos. En un repo público, bots escanean GitHub constantemente y roban keys en minutos. Por eso el primer paso es crear un .gitignore, antes del primer git add.

1. Comandos

Desde la carpeta del proyecto:


bash
git init

# Ignorar secretos y archivos innecesarios
cat > .gitignore << 'EOF'
.env
__pycache__/
*.pyc
venv/
.venv/
instance/
*.db
*.sqlite3
.DS_Store
.vscode/
EOF

# Plantilla de variables sin valores reales (esta sí se sube)
cat > .env.example << 'EOF'
OPENAI_API_KEY=tu_api_key_aqui
DB_PASSWORD=tu_password_aqui
EOF

Verifica que .env quedó excluido:


bash
git status

.env NO debe aparecer en la lista. Si aparece, detente y revisa el .gitignore.


bash
git add .
git commit -m "Primer commit: app Flask"
git branch -M main
2. Crear el repo en GitHub

Entra a github.com → New repository → ponle nombre, márcalo Public y no marques “Add a README” (ya tienes uno). Luego copia la URL y ejecuta:


bash
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main

(Si usas GitHub CLI, es un solo comando: gh repo create nombre-repo --public --source=. --push)

3. Revisa tu código

Asegúrate de que app.py lea los secretos del entorno y no los tenga escritos directamente:


python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]

Busca en tu código si hay alguna contraseña o key escrita a mano. Si la hay, muévela al .env antes del commit. Además, agrega python-dotenv a tu requirements.txt si no está.

Si en algún momento subiste el .env (aunque lo borraras después): revoca la API key en el panel de OpenAI y cambia la contraseña de la base de datos. El historial de Git conserva todo.

4. Plantilla de README

Reemplaza lo que está entre corchetes. Una captura o GIF de la app hace mucha diferencia para quien revisa tu CV.


markdown
# Nombre del Proyecto

Descripción en una o dos frases: qué hace la app y qué problema resuelve.

![Captura de la app](static/screenshot.png)

## Características

- Característica principal 1
- Característica principal 2
- Integración con la API de OpenAI para [qué hace]

## Tecnologías

- Python 3 / Flask
- OpenAI API
- [Base de datos: PostgreSQL / SQLite / MySQL]
- HTML, CSS, Jinja2

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPO.git
   cd TU_REPO
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```


3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   ```bash
   cp .env.example .env
   ```
   Edita `.env` con tu API key de OpenAI y la contraseña de la base de datos.

5. Ejecuta la app:
   ```bash
   flask run
   ```
   Abre http://127.0.0.1:5000 en tu navegador.

## Estructura del proyecto

```
├── app.py            # Aplicación principal
├── templates/        # Plantillas HTML
├── static/           # CSS, JS e imágenes
├── requirements.txt
└── .env.example
```

## Qué aprendí

Un párrafo corto sobre los retos que enfrentaste y qué aprendiste. A los reclutadores les interesa mucho esto.


## Autor

**Tu Nombre** · [LinkedIn](https://linkedin.com/in/tu-perfil) · [Correo](mailto:tu@correo.com)

Para actualizar el README después: edítalo, y luego git add README.md, git commit -m "Agrega README" y git push.

Si quieres, pégame tu app.py (sin las keys) y reviso que no haya secretos escritos a mano o malas prácticas que un reclutador pueda notar.
