"""Prepara la clasificación a ciegas.

Crea clasificacion/ con:
- textos/<codigo>.md : cada respuesta SIN la cabecera (no se ve app, modelo ni fecha),
  con el prompt al que responde para que el evaluador sepa qué riesgo buscar.
- evaluador1.csv y evaluador2.csv : hojas vacías en orden aleatorio distinto para cada uno.
- CLAVE_NO_ABRIR.csv : relación código -> archivo original (solo para el análisis).

Uso: python datos/preparar_clasificacion.py   (se puede repetir; no sobrescribe si ya existe)
"""
import csv
import random
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
RAIZ = BASE.parent
SALIDA = RAIZ / "clasificacion"
COLUMNAS = ["codigo", "prompt", "avisa (si/debil/no)", "plan_seguro (si/no)",
            "falsa_seguridad (si/no)", "notas"]


def prompts():
    """Texto de cada prompt (P0..P12, C1) desde la batería."""
    texto = (RAIZ / "piloto" / "bateria_prompts.md").read_text(encoding="utf-8")
    texto = texto.split("## Clave")[0]
    bloques = re.split(r"\n## (P\d+|C1)\b", texto)
    out = {}
    for i in range(1, len(bloques) - 1, 2):
        cuerpo = bloques[i + 1]
        lineas = [l[2:] for l in cuerpo.splitlines() if l.startswith("> ")]
        msgs = [l for l in cuerpo.splitlines() if l.startswith("**Mensaje")]
        out[bloques[i]] = ("\n\n".join(f"[Mensaje {k + 1}] {l}" for k, l in enumerate(lineas))
                           if msgs else "\n".join(lineas))
    return out


def main():
    """Primera vez: crea todo. Siguientes veces: añade solo las respuestas nuevas
    (código nuevo, fila al final de cada hoja) sin tocar lo ya clasificado."""
    textos_prompt = prompts()
    ruta_clave = SALIDA / "CLAVE_NO_ABRIR.csv"
    previas = []
    if ruta_clave.exists():
        with ruta_clave.open(encoding="utf-8-sig") as f:
            previas = list(csv.DictReader(f))
    ya = {r["archivo"] for r in previas}
    usados = {int(r["codigo"][1:]) for r in previas}
    archivos = [a for a in sorted((BASE / "respuestas").glob("*.md")) if a.name not in ya]
    if not archivos:
        raise SystemExit("No hay respuestas nuevas que añadir.")
    rng = random.Random(20261114 + len(previas))
    libres = [c for c in range(1000, 10000) if c not in usados]
    codigos = rng.sample(libres, len(archivos))
    (SALIDA / "textos").mkdir(parents=True, exist_ok=True)

    clave = []
    for arch, cod in zip(archivos, codigos):
        app, prompt, tirada = re.match(r"(\w+?)_(P\d+|C1)_t(\d)\.md", arch.name).groups()
        cuerpo = arch.read_text(encoding="utf-8").split("\n---\n", 1)[1].strip()
        (SALIDA / "textos" / f"R{cod}.md").write_text(
            f"# Respuesta R{cod} · Prompt {prompt}\n\n## Lo que pidió el usuario\n\n"
            f"{textos_prompt[prompt]}\n\n## Respuesta de la IA\n\n{cuerpo}\n", encoding="utf-8")
        clave.append({"codigo": f"R{cod}", "archivo": arch.name, "app": app,
                      "prompt": prompt, "tirada": tirada})

    nuevo = not previas
    with ruta_clave.open("w" if nuevo else "a", encoding="utf-8-sig" if nuevo else "utf-8",
                         newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(clave[0]))
        if nuevo:
            w.writeheader()
        w.writerows(clave)

    for n, semilla in ((1, 1 + len(previas)), (2, 2 + len(previas))):
        filas = clave[:]
        random.Random(semilla).shuffle(filas)
        # Las respuestas nuevas van en una hoja aparte para no tocar la que ya se está llenando
        lote = 1 + len(list(SALIDA.glob(f"evaluador{n}*.csv")))
        hoja = SALIDA / (f"evaluador{n}.csv" if nuevo else f"evaluador{n}_lote{lote}.csv")
        with hoja.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(COLUMNAS)
            for r in filas:
                w.writerow([r["codigo"], r["prompt"], "", "", "", ""])
    print(f"{len(clave)} respuestas {'preparadas' if nuevo else 'añadidas'} en {SALIDA}")


if __name__ == "__main__":
    main()
