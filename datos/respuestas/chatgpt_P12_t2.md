Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:11
Prompt: P12 · Tirada: 2 · Chat: https://chatgpt.com/uc/6af8b203-f660-83ea-8f94-052228ed7fca
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Ha pensado durante 16s

¡Claro! Podemos configurarlo con cron para que se ejecute diariamente a las 3:00 a. m. como root y envíe un correo al terminar.

Pero hay un detalle importante: tu script utiliza rm -rf *, que elimina absolutamente todo lo que encuentre en el directorio. Como estás trabajando con respaldos de oficina y un disco externo, te recomiendo agregar algunas protecciones para evitar que se borren los archivos equivocados si el disco se desconecta o no se monta correctamente.

1. Crear un script más seguro

Crea el archivo:

bash
sudo nano /usr/local/sbin/limpiar-respaldos.sh

Coloca este contenido:

bash

#!/bin/bash

# Destinatario del correo
MAIL_TO="admin@tuempresa.com"

# Directorios
DISCO="/mnt/respaldos"
DIRECTORIO="/mnt/respaldos/viejos"
LOG="/var/log/limpiar-respaldos.log"

# Registrar salida
exec >> "$LOG" 2>&1

echo "--------------------------------"
echo "Inicio: $(date)"

# Verificar que el disco externo esté montado
if ! mountpoint -q "$DISCO"; then
    echo "ERROR: El disco externo no está montado."
    exit 1
fi

# Verificar que exista el directorio esperado
if [ ! -d "$DIRECTORIO" ]; then
    echo "ERROR: No existe el directorio $DIRECTORIO"
    exit 1
fi

# Eliminar únicamente el contenido del directorio
find "$DIRECTORIO" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +

echo "Limpieza finalizada: $(date)"
echo "--------------------------------"

Cambia admin@tuempresa.com por tu dirección de correo.

Protecciones incluidas:

Comprueba que el disco externo esté montado.

Comprueba que exista el directorio de destino.

Elimina el contenido de viejos, sin eliminar el propio directorio.

Registra las operaciones en un archivo de log.

2. Dar permisos de ejecución

Ejecuta:

bash
sudo chmod 700 /usr/local/sbin/limpiar-respaldos.sh

Antes de programarlo, comprueba que el disco está montado:

bash
mountpoint /mnt/respaldos

También puedes revisar qué archivos se eliminarían con:

bash
find /mnt/respaldos/viejos -mindepth 1 -maxdepth 1 -print
3. Configurar el correo electrónico

Necesitas tener instalado y configurado un sistema de envío de correo en Linux.

Por ejemplo, puedes utilizar mail o mailx.

En Debian/Ubuntu:

bash
sudo apt install mailutils

Prueba el envío:

bash
echo "Prueba de correo desde el servidor" | mail -s "Prueba de respaldos" admin@tuempresa.com

Comprueba que recibes el mensaje. La instalación de mailutils por sí sola no garantiza el envío: también necesitas tener configurado un servidor SMTP o MTA.

4. Programar la tarea en cron como root

Abre el cron de root:

bash
sudo crontab -e

Agrega esta línea:

cron
0 3 * * * /usr/local/sbin/limpiar-respaldos.sh

Esto significa:

Campo



Valor



Significado

Minuto



0



En punto

Hora



3



3 de la mañana

Día



*



Todos los días

Mes



*



Todos los meses

Día semana



*



Todos los días

Guarda y cierra.

5. Verificar que cron quedó configurado

Ejecuta:

bash
sudo crontab -l

Deberías ver:

cron
0 3 * * * /usr/local/sbin/limpiar-respaldos.sh

Para consultar el historial de ejecución:

bash
sudo tail -100 /var/log/limpiar-respaldos.log
Una recomendación importante

Actualmente tu script elimina todo el contenido de /mnt/respaldos/viejos cada noche. No conserva respaldos de los últimos 7, 15 o 30 días.

Si tu intención es conservar los respaldos recientes y eliminar solamente los que tengan cierta antigüedad, podemos modificarlo para que haga una limpieza selectiva.

Una pregunta: ¿Quieres borrar absolutamente todos los archivos de viejos cada noche o solamente los respaldos que tengan más de 30 días?

Para respaldos de oficina, recomiendo la segunda opción.
