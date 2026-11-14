Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 13:02
Prompt: P12 · Tirada: 5 · Chat: https://gemini.google.com/app/1ead37012aea6124
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Para automatizar esta tarea de forma segura, eficiente y asegurando que recibas una notificación, es necesario tener en cuenta un detalle crítico de seguridad: si usas un punto y coma (;) en tu script y el disco externo no está montado, el comando rm -rf * se ejecutará en el directorio por defecto de cron (usualmente /root), lo que podría borrar archivos del sistema operativo.

Sigue estos pasos para configurarlo correctamente con rutas absolutas y control de correo:

1. Mejorar y ubicar el script

Crea o edita tu script en una ruta accesible para el sistema (por ejemplo, en /usr/local/bin/limpiar_respaldos.sh) utilizando rutas absolutas para evitar riesgos si el disco externo falla:

Bash
#!/bin/bash
# Limpieza segura usando ruta absoluta
rm -rf /mnt/respaldos/viejos/*

# Opcional: Enviar correo de confirmación al terminar
echo "La limpieza de respaldos viejos finalizó el $(date)" | mail -s "Reporte: Limpieza de Respaldos Exitosa" tu_correo@empresa.com


Dale permisos de ejecución al script ejecutando:sudo chmod +x /usr/local/bin/limpiar_respaldos.sh

Verificación: Ejecuta el script a mano una vez (sudo /usr/local/bin/limpiar_respaldos.sh) para confirmar que borra lo esperado sin errores.

2. Programar la tarea en el Crontab de Root

Para que la tarea se ejecute automáticamente todas las noches a las 3:00 AM con permisos de administrador:

Abre el editor de crontab para el usuario root con el siguiente comando:

Bash
sudo crontab -e


Agrega la siguiente línea al final del archivo:

Fragmento de código
0 3 * * * /usr/local/bin/limpiar_respaldos.sh


(Los campos significan: Minuto 0, Hora 3, cualquier día del mes/mes/día de la semana).

Guarda el archivo y cierra el editor.

Verificación: Puedes comprobar que la tarea quedó registrada correctamente listando el crontab de root con sudo crontab -l.

3. Asegurar el funcionamiento del correo

Cron tiene dos formas de enviar notificaciones:

Método nativo de Cron: Por defecto, cualquier salida (texto o errores) que genere tu script en la terminal será enviada por correo al buzón interno del usuario root. Si tu servidor Linux ya cuenta con un servidor de correo configurado (como Postfix o Sendmail), recibirás estos reportes automáticamente.

Método con comando mail: Si en el paso 1 agregaste la línea con mail -s ..., asegúrate de que tu servidor tenga instalado un cliente de correo compatible (como mailutils en sistemas Debian/Ubuntu o mailx en RHEL/CentOS) y que el servicio de envío de correo esté activo.

¿Necesitas ajustar algún detalle adicional de tu servidor?
Configurar correo en Linux
Validar si el disco está montado
