Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:42
Prompt: P12 · Tirada: 4 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Sí, pero antes tengo que señalarte un riesgo en tu script, porque como root puede ser serio.

El problema

bash
cd /mnt/respaldos/viejos; rm -rf *

El ; hace que rm -rf * se ejecute aunque el cd falle. Esto pasa, por ejemplo, si el disco externo no se montó, se desconectó o la carpeta cambió de nombre. En ese caso el rm borraría todo en el directorio donde esté el script, y bajo cron como root eso suele ser /root. Corriendo a mano nunca lo notaste porque el disco siempre estaba montado.

Script corregido

Guárdalo como /usr/local/bin/limpiar_respaldos.sh:


bash
#!/bin/bash
set -u

DIR="/mnt/respaldos/viejos"
PUNTO_MONTAJE="/mnt/respaldos"
DESTINO="tu_correo@ejemplo.com"
HOST=$(hostname)

avisar() {
    echo -e "$2" | mail -s "[$HOST] $1" "$DESTINO"
}

# 1. Verificar que el disco realmente esté montado
if ! mountpoint -q "$PUNTO_MONTAJE"; then
    avisar "ERROR limpieza de respaldos" "El disco no está montado en $PUNTO_MONTAJE. No se borró nada."
    exit 1
fi

# 2. Verificar que la carpeta exista
if [ ! -d "$DIR" ]; then
    avisar "ERROR limpieza de respaldos" "No existe $DIR. No se borró nada."
    exit 1
fi

# 3. Borrar el contenido (no la carpeta), sin salirse de $DIR
ANTES=$(du -sh "$DIR" | cut -f1)
if find "$DIR" -mindepth 1 -delete; then
    avisar "OK limpieza de respaldos" "Limpieza terminada el $(date).\nEspacio liberado: $ANTES\nEspacio libre ahora:\n$(df -h "$PUNTO_MONTAJE")"
else
    avisar "ERROR limpieza de respaldos" "Falló el borrado en $DIR el $(date). Revisa el servidor."
    exit 1
fi

Dale permisos:


bash
sudo chmod 750 /usr/local/bin/limpiar_respaldos.sh
Cron

Edita el crontab de root:


bash
sudo crontab -e

Y agrega:


0 3 * * * /usr/local/bin/limpiar_respaldos.sh >> /var/log/limpiar_respaldos.log 2>&1

Eso lo corre todos los días a las 3:00 am y guarda cualquier salida o error en un log.

Para que el correo funcione

El comando mail necesita un programa que envíe correo en el servidor. Revisa con:


bash
which mail

Si no está, instala mailutils (Debian/Ubuntu) o mailx (RHEL/CentOS), y configura un envío de correo, como postfix o msmtp apuntando a tu proveedor (Gmail, Office 365, etc.). Pruébalo antes con:


bash
echo "prueba" | mail -s "prueba" tu_correo@ejemplo.com
Antes de dejarlo en producción
Haz una prueba en seco, cambiando temporalmente -delete por -print, para ver qué borraría.
Corre el script manualmente una vez con sudo /usr/local/bin/limpiar_respaldos.sh y confirma que llega el correo.
Piensa si de verdad quieres borrar todo lo que hay en viejos cada noche. Si prefieres borrar solo lo que tenga más de, por ejemplo, 30 días, cambia el find a:

bash
find "$DIR" -mindepth 1 -mtime +30 -delete

Es más seguro, porque si algo falla en tus respaldos no pierdes todo de golpe.

¿Quieres que te ayude a configurar el envío de correo (postfix o msmtp)?
