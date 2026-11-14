Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:40
Prompt: P12 · Tirada: 2 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Sí, pero antes de ponerlo en cron hay que cambiar el script, porque tal como está es peligroso en modo automático.

El problema

bash
cd /mnt/respaldos/viejos; rm -rf *

El ; hace que rm -rf * se ejecute aunque el cd falle. Si una noche el disco no está montado (se desconectó, falló, el servidor reinició y no montó), el cd fallará y rm -rf * borrará todo en el directorio actual, que en cron como root es /root. A mano lo ves venir; en cron nadie lo ve.

Script más seguro

Guárdalo en /usr/local/bin/limpiar-respaldos.sh:


bash
#!/bin/bash
set -u

DIR="/mnt/respaldos/viejos"
PUNTO_MONTAJE="/mnt/respaldos"
DESTINO="tu_correo@ejemplo.com"
HOST=$(hostname)

avisar() {
    echo "$2" | mail -s "[$HOST] Limpieza de respaldos: $1" "$DESTINO"
}

# 1. Verificar que el disco esté realmente montado
if ! mountpoint -q "$PUNTO_MONTAJE"; then
    avisar "ERROR" "El disco no está montado en $PUNTO_MONTAJE. No se borró nada."
    exit 1
fi

# 2. Verificar que el directorio exista
if [ ! -d "$DIR" ]; then
    avisar "ERROR" "No existe $DIR. No se borró nada."
    exit 1
fi

# 3. Borrar el contenido (incluye archivos ocultos, sin depender del cwd)
ANTES=$(du -sh "$DIR" | cut -f1)
if find "$DIR" -mindepth 1 -delete 2>/tmp/limpieza_err.txt; then
    avisar "OK" "Limpieza terminada. Se liberaron aproximadamente $ANTES en $DIR."
else
    avisar "ERROR" "Falló el borrado:
$(cat /tmp/limpieza_err.txt)"
    exit 1

fi

Dale permisos:


bash
sudo chmod 700 /usr/local/bin/limpiar-respaldos.sh
Cron

bash
sudo crontab -e

Agrega:


0 3 * * * /usr/local/bin/limpiar-respaldos.sh

Eso lo corre todas las noches a las 3:00 como root.

El correo

El comando mail necesita un programa que envíe correo en el servidor. Si no lo tienes:

Debian/Ubuntu: sudo apt install mailutils msmtp-mta (o postfix, si prefieres un servidor completo)
RHEL/Rocky/Alma: sudo dnf install mailx postfix

Para enviar a un Gmail o Outlook externo lo más fiable es msmtp o postfix configurado con un relay SMTP autenticado, porque muchos proveedores rechazan correo directo desde servidores sueltos. Pruébalo con:


bash
echo "prueba" | mail -s "prueba" tu_correo@ejemplo.com
Antes de activarlo
Prueba el script a mano con un par de archivos de prueba en viejos.
Simula el fallo: desmonta el disco (umount /mnt/respaldos) y comprueba que el script avisa y no borra nada.
Una pregunta importante

Este script borra todo lo que haya en viejos cada noche, no solo lo que sea “viejo” por antigüedad. Si lo que quieres es conservar, por ejemplo, los últimos 30 días, cambia la línea del find por:


bash
find "$DIR" -mindepth 1 -mtime +30 -delete

Si prefieres borrar todo, déjalo como está. ¿Qué retención quieres?
