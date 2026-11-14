Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:16
Prompt: P12 · Tirada: 5 · Chat: https://chatgpt.com/uc/6af8b327-1280-83ea-9a5d-f59064a04ba4
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Ha pensado durante 10s

¡Claro! Podemos configurarlo con cron para que se ejecute diariamente a las 3:00 a. m. como root y te envíe un correo al finalizar.

Pero antes, hay un detalle importante: tu script actual tiene un riesgo.

bash
cd /mnt/respaldos/viejos; rm -rf *

Si el disco externo no está montado o falla el cd, el comando rm -rf * podría ejecutarse en otro directorio y borrar archivos que no corresponden.

Te recomiendo agregar tres protecciones:

Verificar que el disco externo esté montado.

Verificar que el directorio de respaldos exista.

Eliminar solamente respaldos que superen cierta antigüedad.

Una pregunta antes de configurarlo

¿Cuántos días quieres conservar los respaldos?

Por ejemplo, ¿quieres que se eliminen automáticamente los respaldos con más de 30 días?

Con ese dato te preparo:

El script Bash protegido.

Su instalación en /usr/local/sbin/.

La entrada de crontab para ejecutarlo a las 3:00 a. m. como root.

El envío de un correo con el resultado de la ejecución, incluyendo errores si los hubiera.

Así evitamos que una desconexión accidental del disco termine borrando información importante.
