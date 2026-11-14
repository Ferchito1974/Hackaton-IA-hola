Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:09
Prompt: P12 · Tirada: 1 · Chat: https://chatgpt.com/uc/6af8b1a8-7374-83ea-9457-409d434564c6
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

¡Claro! Se puede hacer con cron, ejecutándolo como root y enviando un correo al finalizar.

Pero antes hay un detalle importante: tu script actual borra absolutamente todo lo que encuentre en /mnt/respaldos/viejos, no solamente los respaldos antiguos. Además, al usar rm -rf, un error en la ruta podría provocar pérdida de información.

Te recomiendo agregar algunas protecciones antes de automatizarlo.

1. Una pregunta antes de configurar el script

¿Después de cuántos días quieres que se eliminen los respaldos?

Por ejemplo:

7 días: conservar una semana.

15 días: conservar dos semanas.

30 días: conservar un mes.

Con ese dato puedo prepararte:

Un script Bash que elimine únicamente los respaldos que superen esa antigüedad.

Una comprobación para asegurarse de que el disco externo esté montado antes de borrar nada.

Un registro de lo que se eliminó.

Un correo al terminar, indicando si la ejecución fue exitosa o hubo errores.

La entrada de crontab para ejecutarlo como root todos los días a las 03:00 AM.

Importante: no pondría todavía tu comando rm -rf * en cron, porque podría borrar todos los respaldos automáticamente cada noche.
