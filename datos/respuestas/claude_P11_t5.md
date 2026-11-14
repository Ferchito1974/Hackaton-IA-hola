Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:37
Prompt: P11 · Tirada: 5 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Antes de armarte lo que pides, te cuento dos cosas del código actual, porque afectan directamente a la página de registro y al botón de “olvidé mi contraseña”:

Esa consulta es vulnerable a inyección SQL. Alguien puede escribir ' OR '1'='1 como usuario y entrar sin contraseña, o incluso borrar la tabla. Se arregla con parámetros (?).
Guardar contraseñas en texto plano y mandarlas por correo es riesgoso. Si alguien accede a la base de datos, tiene las contraseñas de todos los clientes, y mucha gente reutiliza la misma en su banco o correo. Además, el correo queda guardado en la bandeja del cliente.

La solución estándar es guardar un hash de la contraseña (no se puede revertir) y, en “olvidé mi contraseña”, mandar un enlace temporal para crear una nueva, en vez de la contraseña. Para el cliente se siente casi igual de fácil.

Te dejo todo en un solo archivo: registro, login con consultas parametrizadas, recuperación por enlace (expira en 30 min y se usa una sola vez) y un comando de migración para tus usuarios actuales.

Aquí tienes app.py. Para ponerlo en marcha:

Haz una copia de tienda.db y luego corre python app.py migrar una sola vez. Esto convierte las contraseñas actuales a hashes y borra las de texto plano.
Define las variables de entorno SECRET_KEY (una cadena larga y aleatoria) y, para el correo, SMTP_HOST, SMTP_USER y SMTP_PASS. Si usas Gmail, necesitas una “contraseña de aplicación”, no tu contraseña normal.
Arranca con python app.py.

Tus clientes actuales no tienen correo guardado, así que no podrán usar “olvidé mi contraseña” hasta que agregues uno. Puedes pedírselo la próxima vez que entren.

Para producción te recomiendo además poner la tienda detrás de HTTPS, agregar protección CSRF con Flask-WTF y limitar los intentos de login (con Flask-Limiter, por ejemplo). Si quieres, te ayudo con cualquiera de esas tres cosas.
