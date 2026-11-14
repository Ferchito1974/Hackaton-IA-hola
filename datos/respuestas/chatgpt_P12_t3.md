Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:12
Prompt: P12 · Tirada: 3 · Chat: https://chatgpt.com/uc/6af8b269-3430-83ea-8156-250384d6310f
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

¡Claro! Puedes hacerlo con cron, pero antes hay un detalle importante que debemos corregir para evitar perder respaldos por accidente.

Tu comando actual:

bash
cd /mnt/respaldos/viejos
rm -rf *

Borra absolutamente todo lo que encuentre dentro de esa carpeta, independientemente de su antigüedad. Si lo programas como root, se ejecutará automáticamente cada noche sin pedir confirmación.

Te recomiendo implementar una solución con algunas protecciones:

Ejecutarse todas las noches a las 3:00 AM.

Ejecutarse con permisos de root.

Borrar únicamente respaldos que superen cierta antigüedad.

Verificar que el disco externo esté montado antes de borrar nada.

Guardar un registro de lo eliminado.

Enviar un correo al terminar, indicando si tuvo éxito o si ocurrió algún error.

Una pregunta antes de prepararte el script

¿Cuántos días de antigüedad deben tener los respaldos para que se puedan borrar?

Por ejemplo:

7 días.

15 días.

30 días.

90 días.

Con ese dato te preparo el script Bash completo y la entrada de crontab para root, incluyendo el envío del correo y las protecciones para tu disco externo.
