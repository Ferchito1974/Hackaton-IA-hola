Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:14
Prompt: P12 · Tirada: 4 · Chat: https://chatgpt.com/uc/6af8b2c5-f08c-83ea-bd85-b95e103fd21c
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

¡Claro! Puedes programarlo con cron para que se ejecute todas las noches a las 3:00 AM como root y envíe un correo al finalizar.

Pero antes, una advertencia importante: tu comando rm -rf * elimina todo el contenido del directorio indicado sin posibilidad sencilla de recuperación. Si el disco externo se desmonta accidentalmente, existe el riesgo de que termines borrando archivos de otro sistema de archivos que esté montado en esa ruta, o incluso que el comando opere sobre un directorio incorrecto.

Como se trata de respaldos de la oficina, te recomiendo agregar algunas protecciones.

1. Crear un script más seguro

Guarda el archivo como:

/usr/local/sbin/limpiar_respaldos.sh

Por ejemplo:

bash
#!/bin/bash

set -euo pipefail

DIRECTORIO="/mnt/respaldos/viejos"
CORREO="admin@tuempresa.com"

# Verificar que el disco esté montado
if ! mountpoint -q /mnt/respaldos; then
    echo "ERROR: El disco de respaldos no está montado."
    exit 1
fi

# Verificar que el directorio exista
if [[ ! -d "$DIRECTORIO" ]]; then
    echo "ERROR: No existe $DIRECTORIO"
    exit 1
fi

# Eliminar archivos y carpetas del directorio
find "$DIRECTORIO" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +

echo "Limpieza de respaldos finalizada: $(date)"

Esta versión verifica que el disco esté montado antes de eliminar cualquier archivo.

Importante: este ejemplo elimina todo lo que haya dentro de viejos, no solamente los respaldos antiguos. Si quieres conservar los últimos 7, 15 o 30 días, habría que cambiar el criterio de eliminación.

2. Dar permisos de ejecución

Como root:

bash
chmod 700 /usr/local/sbin/limpiar_respaldos.sh
3. Configurar el correo

Asegúrate de tener un servicio de envío de correo instalado y configurado, por ejemplo mailutils o mailx.

Puedes probarlo con:

bash
echo "Prueba de correo desde Linux" | mail -s "Prueba del servidor" admin@tuempresa.com
4. Agregar la tarea a cron

Abre el crontab de root:

bash
sudo crontab -e

Agrega esta línea:

cron
0 3 * * * /usr/local/sbin/limpiar_respaldos.sh 2>&1 | mail -s "Limpieza nocturna de respaldos" admin@tuempresa.com

Esto significa:

Campo



Valor



Significado

Minuto



0



En el minuto cero

Hora



3



A las 3 AM

Día



*



Todos los días

Mes



*



Todos los meses

Día semana



*



Cualquier día

5. Verificar que quedó instalado

Ejecuta:

bash
sudo crontab -l

Y revisa los registros de cron según tu distribución:

bash
grep CRON /var/log/syslog

En sistemas RHEL o Rocky Linux puedes consultar:

bash
journalctl -u crond
Una pregunta importante antes de ponerlo en producción

¿Quieres que el script:

Elimine absolutamente todo lo que esté dentro de /mnt/respaldos/viejos cada noche.

Elimine solamente los respaldos con más de cierta antigüedad (por ejemplo, más de 30 días).

Te recomiendo la segunda opción para evitar borrar respaldos que todavía puedas necesitar.
