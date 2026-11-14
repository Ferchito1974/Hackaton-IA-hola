"""Copia una captura del navegador a datos/capturas/<nombre>.jpg.

Uso: python guardar_captura.py <ruta_jpg_de_la_captura> <app>_<prompt>_t<tirada>[_parte]
La ruta es la que muestra la herramienta screenshot ("source: ...jpg").
"""
import shutil
import sys
from pathlib import Path

DESTINO = Path(__file__).resolve().parent / "capturas"

origen, nombre = Path(sys.argv[1]), sys.argv[2]
destino = DESTINO / f"{nombre}.jpg"
if not origen.exists():
    sys.exit(f"No existe la captura {origen}")
if destino.exists():
    sys.exit(f"{destino.name} ya existe: no se sobrescribe.")
DESTINO.mkdir(exist_ok=True)
shutil.copy2(origen, destino)
print(f"OK {destino.name}")
