"""Guarda una respuesta del estudio: un .md en respuestas/ y una fila en respuestas.csv.

Uso: python guardar.py <app> <modelo> <prompt> <tirada> <url> < texto_respuesta
"""
import csv
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
CSV = BASE / "respuestas.csv"
CARPETA = BASE / "respuestas"


def main():
    app, modelo, prompt, tirada, url = sys.argv[1:6]
    texto = sys.stdin.buffer.read().decode("utf-8").strip()
    if len(texto) < 50:
        sys.exit("Respuesta vacía o demasiado corta: no se guarda.")

    nombre = f"{app}_{prompt}_t{tirada}.md"
    destino = CARPETA / nombre
    if destino.exists():
        sys.exit(f"{nombre} ya existe: no se sobrescribe.")

    ahora = datetime.now()
    fecha, hora = ahora.strftime("%Y-%m-%d"), ahora.strftime("%H:%M")
    CARPETA.mkdir(exist_ok=True)
    destino.write_text(
        f"Modelo: {modelo} · App: {app} · Sin sesión · {fecha} {hora}\n"
        f"Prompt: {prompt} · Tirada: {tirada} · Chat: {url}\n"
        f"Recogido por Claude con el navegador integrado (chat nuevo por tirada).\n\n---\n\n{texto}\n",
        encoding="utf-8",
    )

    with CSV.open(encoding="utf-8-sig") as f:
        filas = list(csv.reader(f))
    nuevo_id = len([r for r in filas[1:] if r]) + 1
    with CSV.open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow(
            [nuevo_id, fecha, hora, app, modelo, "sin", prompt, tirada, nombre, "", "", "", ""]
        )
    print(f"OK id={nuevo_id} {nombre} ({len(texto)} caracteres)")


if __name__ == "__main__":
    main()
