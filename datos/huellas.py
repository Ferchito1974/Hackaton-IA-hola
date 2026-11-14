"""Genera datos/HUELLAS.sha256 con el SHA-256 de cada respuesta y captura.

Si alguien cambia un solo carácter de una respuesta, su huella deja de coincidir.
Uso: python datos/huellas.py
"""
import hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parent
lineas = []
for carpeta in ("respuestas", "capturas"):
    for f in sorted((BASE / carpeta).glob("*")):
        if f.is_file():
            lineas.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {carpeta}/{f.name}")
lineas.append(f"{hashlib.sha256((BASE / 'respuestas.csv').read_bytes()).hexdigest()}  respuestas.csv")
(BASE / "HUELLAS.sha256").write_text("\n".join(lineas) + "\n", encoding="utf-8")
print(f"{len(lineas)} huellas")
