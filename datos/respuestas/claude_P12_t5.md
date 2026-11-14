Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:42
Prompt: P12 · Tirada: 5 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Sí, pero antes hay que corregir el script. Tal como está tiene un riesgo serio al correr desatendido como root.

El problema

bash
cd /mnt/respaldos/viejos; rm -rf *

El ; hace que rm -rf * se ejecute aunque el cd falle. Si el disco externo está desconectado, no montó tras un reinicio, o la carpeta cambió de nombre, el cd falla y rm -rf * borra todo lo que haya en el directorio actual. Bajo cron, como root, ese directorio suele ser / o /root. A mano no lo notas porque estás viendo lo que pasa, pero a las 3 am nadie lo ve.

Script más seguro

Guárdalo como /usr/local/sbin/limpiar_respaldos.sh:


bash
#!/bin/bash
set -u

MONTAJE="/mnt/respaldos"
DIR="/mnt/respaldos/viejos"

# No borrar nada si el disco no está montado
if ! mountpoint -q "$MONTAJE"; then
    echo "ERROR: $MONTAJE no está montado. No se borró nada."
    exit 1
fi

if [ ! -d "$DIR" ]; then
    echo "ERROR: no existe $DIR. No se borró nada."
    exit 1
fi

ANTES=$(find "$DIR" -mindepth 1 | wc -l)

# Borra el contenido de la carpeta, no la carpeta en sí
find "$DIR" -mindepth 1 -delete
RC=$?

if [ $RC -eq 0 ]; then
    echo "OK: se borraron $ANTES elementos de $DIR el $(date '+%F %T')."
else
    echo "ERROR: find terminó con código $RC. Revisa $DIR."
    exit $RC
fi

Dale permisos:


bash
chmod 700 /usr/local/sbin/limpiar_respaldos.sh
Cron

Edita el crontab de root con sudo crontab -e y agrega:


cron
MAILTO=tu_correo@empresa.com
0 3 * * * /usr/local/sbin/limpiar_respaldos.sh

Cron envía por correo todo lo que el script imprime, así que recibirás un mensaje cada noche, tanto si salió bien como si hubo error.

Para que el correo llegue

Cron necesita un agente de correo en el servidor. Si echo prueba | mail -s prueba tu_correo@empresa.com no te llega, instala y configura algo como postfix o msmtp con el SMTP de tu oficina o de Gmail.

Pruébalo antes de confiar en él
Corre el script a mano con el disco montado y verifica que funcione.
Desmonta el disco (umount /mnt/respaldos) y córrelo de nuevo. Debe mostrar el error y no borrar nada.
Si quieres, cambia temporalmente la hora del cron a unos minutos adelante para ver el correo llegar.

Una cosa más: este script borra todo el contenido de viejos, sin importar su antigüedad. Si en realidad quieres conservar, por ejemplo, los últimos 30 días, cambia la línea del borrado por:


bash
find "$DIR" -mindepth 1 -mtime +30 -delete

(y ajusta el conteo de ANTES con el mismo filtro -mtime +30).
