"""Traduce al inglés todas las respuestas (datos/respuestas/*.md) con Argos Translate, sin conexión.

Escribe datos/respuestas_en/<mismo nombre>.md: cabecera original + aviso de traducción automática + texto
traducido línea a línea (se conservan saltos de línea, listas y tablas). Los originales en español no se tocan
y son la evidencia del estudio; las traducciones son solo para lectura.

Uso: python datos/traducir_respuestas.py        (salta las que ya existen)
"""
from pathlib import Path

import argostranslate.translate as tr

BASE = Path(__file__).resolve().parent
ORIG, DEST = BASE / "respuestas", BASE / "respuestas_en"
AVISO = ("Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/{name}`, for reading only. "
         "The Spanish original is the evidence used in the study; wording here may be imprecise.")


def traducir_linea(linea):
    s = linea.strip()
    if not s or not any(c.isalpha() for c in s):
        return linea
    sangria = linea[: len(linea) - len(linea.lstrip())]
    return sangria + tr.translate(s, "es", "en")


def main():
    DEST.mkdir(exist_ok=True)
    archivos = sorted(ORIG.glob("*.md"))
    hechos = 0
    for f in archivos:
        out = DEST / f.name
        if out.exists():
            continue
        texto = f.read_text(encoding="utf-8")
        cabecera, cuerpo = texto.split("\n---\n", 1) if "\n---\n" in texto else ("", texto)
        traducido = "\n".join(traducir_linea(l) for l in cuerpo.split("\n"))
        out.write_text(f"{cabecera.strip()}\n\n> {AVISO.format(name=f.name)}\n\n---\n{traducido}", encoding="utf-8")
        hechos += 1
        print(f"{hechos}: {f.name}", flush=True)
    print(f"Listo: {hechos} traducidas, {len(archivos)} en total")


if __name__ == "__main__":
    main()
