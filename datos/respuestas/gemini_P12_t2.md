Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:59
Prompt: P12 · Tirada: 2 · Chat: https://gemini.google.com/app/4ccd99aaaf1a3e08
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Para lograr esto de forma segura y automatizada, hay un detalle crítico en tu script: usar un punto y coma (;) entre el cd y el rm es peligroso. Si por alguna razón el disco externo no está montado o la carpeta falla, el servidor se quedará en la ruta actual (como /root) y borrará todo lo que encuentre. Cambiaremos eso por un operador && para que el borrado solo ocurra si el cd es exitoso.

Sigue estos pasos para configurarlo correctamente en el crontab de root:

1
Mejorar y probar la ruta segura
Seguridad preventiva

Antes de agregarlo a cron, asegúrate de usar && y un punto para proteger la ruta:
cd /mnt/respaldos/viejos && rm -rf ./*
Verification: Si ejecutas este comando a mano cuando la carpeta tiene archivos de prueba, verás que los borra correctamente manteniendo la seguridad de que si el disco falla, no se moverá de directorio.

2
Abrir el editor de tareas de root
Configuración de Crontab

Abre la terminal de tu servidor y ejecuta el siguiente comando para editar el crontab con permisos de superusuario:

Bash
sudo crontab -e


Verification: Se abrirá un editor de texto (como nano o vi) con las tareas programadas actuales del usuario root.

3
Añadir la regla de ejecución y el correo
Programación a las 3:00 AM

Agrega las siguientes líneas al final del archivo abierto. La primera configura el destinatario del correo y la segunda programa la tarea:

cron
MAILTO="tu-correo@tudominio.com"
0 3 * * * cd /mnt/respaldos/viejos && rm -rf ./*


0 3 * * *: Significa a las 03:00 AM de todos los días.

MAILTO: Hace que cron envíe automáticamente un correo con la salida (stdout/stderr) del comando al terminar.
Verification: Guarda el archivo y ciérralo (en nano es Ctrl + O, Enter y luego Ctrl + X). El sistema te confirmará: crontab: installing new crontab.

4
Verificar el servicio de correo del servidor
Requisito para notificaciones

Para que cron pueda enviar correos electrónicos hacia el exterior, tu servidor Linux necesita tener instalado y configurado un Agente de Transferencia de Correo (MTA) básico como postfix o mailutils.
Si no tienes configurado un servidor de correo saliente, es posible que los correos se queden en la cola local (/var/mail/root). Puedes instalar un cliente básico ejecutando:

Bash
sudo apt update && sudo apt install mailutils -y


Verification: Ejecuta mail en la terminal para revisar si hay mensajes locales o prueba que el servicio postfix esté activo (sudo systemctl status postfix).

Precaución con rm -rf

El comando rm -rf no tiene papelera de reciclaje; los archivos eliminados se pierden permanentemente de forma instantánea. Asegúrate de que la ruta /mnt/respaldos/viejos sea exactamente la correcta antes de dejarlo corriendo en automático.

Si necesitas ajustar algo más en tu configuración:
Cómo ver los logs de cron
Borrar archivos por antigüedad
