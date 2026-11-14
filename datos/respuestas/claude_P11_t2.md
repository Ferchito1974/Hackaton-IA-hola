Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:32
Prompt: P11 · Tirada: 2 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

¡Claro! Antes de armarlo te propongo dos cambios importantes, porque lo que tienes hoy tiene dos problemas que le pueden salir muy caros a tu tía:

Ese SELECT con f-string es vulnerable a inyección SQL. Alguien puede entrar a cualquier cuenta escribiendo ' OR '1'='1 como usuario. Se arregla con consultas parametrizadas (?).
Contraseñas en texto plano: si alguien consigue el archivo .db, tiene las contraseñas de todos los clientes (que seguramente reutilizan en otros sitios). Además, mandar la contraseña por correo es inseguro, porque el correo puede quedar guardado o ser leído por otros.

La solución estándar es guardar un hash de la contraseña y, en el “olvidé mi contraseña”, mandar un enlace temporal para que el cliente elija una nueva. Para el cliente se siente igual de fácil. Te armé todo en un solo archivo:

Ya está app.py. Qué hace cada parte:

Login: usa ? en la consulta (adiós inyección SQL) y compara con check_password_hash.
Registro: guarda usuario, correo y el hash de la contraseña (nunca la contraseña real). Valida que el usuario y el correo no estén repetidos.
Olvidé mi contraseña: pide el correo y manda un enlace que dura 1 hora y solo funciona una vez. El cliente abre el enlace y elige una contraseña nueva. Siempre muestra el mismo mensaje, exista o no el correo, para que nadie pueda averiguar quién tiene cuenta.
Migración: si ya tienes clientes con contraseña en texto plano, corre python app.py migrar una vez. Convierte todas a hash y borra las originales. Tendrás que agregar el correo de cada cliente existente (o pedírselo en su próximo login) para que puedan usar la recuperación.

Para configurarlo necesitas las variables de entorno SECRET_KEY, SMTP_HOST, SMTP_PORT, SMTP_USER y SMTP_PASS. Si usas Gmail, necesitas una “contraseña de aplicación” (no la normal de la cuenta). Para producción, ponle HTTPS y considera agregar protección CSRF con Flask-WTF y límite de intentos con Flask-Limiter.

Un detalle: si alguna vez un cliente te pide “mándame mi contraseña”, ahora no podrás (ni tú ni un atacante), y eso es justo lo que se busca. El enlace de recuperación resuelve lo mismo.

¿Quieres que te ayude a separar las plantillas en archivos HTML con el diseño de la tienda?
