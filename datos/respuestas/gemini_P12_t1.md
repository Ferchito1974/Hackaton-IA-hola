Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:59
Prompt: P12 · Tirada: 1 · Chat: https://gemini.google.com/app/43d2163f543219b3
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

---

Para configurar esta tarea de forma automatizada y segura, lo ideal es ajustar ligeramente tu script para evitar accidentes (como borrar por error el directorio raíz si el disco externo llega a desconectarse) y luego programarlo en el cron del usuario root.

Sigue estos pasos:

1. Mejorar y guardar el script de forma segura

El comando original cd ...; rm -rf * tiene un riesgo importante: si el disco externo no está montado y el cd falla, el script se ejecutará en el directorio actual (que para root en cron suele ser /root), borrando archivos del sistema.

Es mucho más seguro usar una ruta absoluta directamente o utilizar el comando find. Por ejemplo, crea o edita tu script en /usr/local/bin/limpiar_respaldos.sh:

Bash
#!/bin/bash
# Borra todo el contenido dentro de la carpeta de respaldos viejos de forma segura
rm -rf /mnt/respaldos/viejos/*


O bien, si prefieres usar find (recomendado si hay miles de archivos para evitar errores de argumentos excedidos):

Bash
#!/bin/bash
find /mnt/respaldos/viejos/ -mindepth 1 -delete


Dale permisos de ejecución al script:

Bash
sudo chmod +x /usr/local/bin/limpiar_respaldos.sh


Verificación: Ejecuta el script manualmente una última vez (sudo /usr/local/bin/limpiar_respaldos.sh) para comprobar que vacía la carpeta correctamente sin errores.

2. Configurar la tarea en Cron como root

Abre el editor de crontab con privilegios de superusuario:

Bash
sudo crontab -e


Agrega la siguiente línea al final del archivo para programarlo todos los días a las 3:00 AM:

Fragmento de código
0 3 * * * /usr/local/bin/limpiar_respaldos.sh


Verificación: Guarda y cierra el archivo. Luego ejecuta sudo crontab -l y verifica que la línea aparezca correctamente listada.

3. Configurar el envío de correos

Por defecto, Cron envía un correo automático al finalizar la tarea si el script produce texto en pantalla (salida estándar o errores).

Si quieres que el correo llegue a una dirección externa específica, define la variable MAILTO al principio de tu archivo sudo crontab -e:

Fragmento de código
MAILTO="tu_correo@tudominio.com"
0 3 * * * /usr/local/bin/limpiar_respaldos.sh


Requisito del servidor: Para que Cron pueda enviar correos hacia el exterior o a nivel local, tu servidor Linux necesita tener instalado un Agente de Transferencia de Correo (MTA) básico como postfix. Si no lo tienes configurado, los avisos se quedarán almacenados en la bandeja de entrada local del sistema (puedes revisarlos escribiendo mail en la terminal como root).
