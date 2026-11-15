"""Genera clasificacion/clasificador.html: una herramienta en el navegador para clasificar.

Cada evaluador abre el archivo, elige si es el evaluador 1 o 2 y ve las respuestas en SU orden
(el de su hoja), una por una, sin saber de qué app son. Marca sus respuestas con botones, el avance
se guarda en el navegador y al final descarga su CSV (mismo formato que evaluadorN.csv).

Uso: python datos/generar_clasificador.py
"""
import csv
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CLAS = RAIZ / "clasificacion"


def clave_riesgos():
    texto = (RAIZ / "piloto" / "bateria_prompts.md").read_text(encoding="utf-8").split("## Clave", 1)[1]
    return {m.group(1): re.sub(r"\*\*", "", m.group(2)).strip()
            for m in re.finditer(r"- \*\*(P\d+|C1)[^*]*:\*\* (.+)", texto)}


def orden(n):
    with (CLAS / f"evaluador{n}.csv").open(encoding="utf-8-sig") as f:
        return [r["codigo"] for r in csv.DictReader(f)]


def main():
    textos = {}
    for p in sorted((CLAS / "textos").glob("R*.md")):
        t = p.read_text(encoding="utf-8")
        prompt = re.search(r"· Prompt (P\d+|C1)", t).group(1)
        pedido = t.split("## Lo que pidió el usuario", 1)[1].split("## Respuesta de la IA", 1)[0].strip()
        respuesta = t.split("## Respuesta de la IA", 1)[1].strip()
        textos[p.stem] = {"prompt": prompt, "pedido": pedido, "respuesta": respuesta}
    datos = {"textos": textos, "clave": clave_riesgos(), "orden": {"1": orden(1), "2": orden(2)}}
    plantilla = (Path(__file__).parent / "clasificador_plantilla.html").read_text(encoding="utf-8")
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    (CLAS / "clasificador.html").write_text(plantilla.replace("/*DATOS*/null", js), encoding="utf-8")
    print(f"clasificacion/clasificador.html: {len(textos)} respuestas")


if __name__ == "__main__":
    main()
