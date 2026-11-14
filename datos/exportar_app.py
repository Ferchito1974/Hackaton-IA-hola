"""Genera app/data.js con todo lo que necesita la app de visualización.

Incluye: los prompts (título, área, dificultad, texto, riesgo de la clave), todas las respuestas
(texto literal, app, modelo, sesión, fecha, captura) y, si existen, los resultados del análisis
(resultados/resultados.json; si no, resultados_demo/ marcado como DEMO).

Uso: python datos/exportar_app.py   (volver a correrlo cada vez que cambien datos o resultados)
"""
import csv
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "datos"
APP = RAIZ / "app"

AREA = {"P0": "Salud", "P2": "Salud", "P5": "Salud", "P7": "Salud", "P8": "Salud", "C1": "Salud (control)",
        "P3": "Seguridad infantil", "P4": "Alimentación",
        "P1": "Ingeniería", "P6": "Ingeniería", "P9": "Ingeniería",
        "P10": "Informática", "P11": "Informática", "P12": "Informática"}
DIFICULTAD = {"P0": "sencillo", "P1": "sencillo", "P10": "sencillo", "P5": "medio", "P6": "medio",
              "P11": "medio", "P8": "complejo", "P9": "complejo", "P12": "complejo"}
# Palabras que la app resalta para encontrar rápido dónde se habla del riesgo (no es una clasificación)
RESALTAR = {
    "P0": ["toronja", "simvastatina", "estatina"], "P7": ["toronja", "simvastatina", "estatina"],
    "C1": ["toronja", "pravastatina", "estatina"], "P1": ["de carga", "estructural", "ingeniero"],
    "P2": ["hipoglucemia", "insulina", "médico", "glargina"], "P3": ["asfixia", "atragant", "uvas", "cacahuate", "palomitas"],
    "P4": ["gluten", "tamari", "soya", "trigo"], "P5": ["serotonin", "San Juan", "5-HTP"],
    "P6": ["circuito", "amper", "calibre", "electricista", "interruptor"], "P8": ["semanal", "semana", "metotrexato"],
    "P9": ["transferencia", "retroaliment", "macho", "electrocu", "monóxido"], "P10": [".gitignore", ".env"],
    "P11": ["inyección", "injection", "hash", "parametriz"], "P12": ["|| exit", "set -e", "montad", "mountpoint", "si el cd"],
}


def leer_bateria():
    texto = (RAIZ / "piloto" / "bateria_prompts.md").read_text(encoding="utf-8")
    cuerpo, clave = texto.split("## Clave", 1)
    prompts = {}
    for m in re.finditer(r"\n## (P\d+|C1)\.? ?([^\n]*)\n(.*?)(?=\n## |\Z)", cuerpo, re.S):
        pid, titulo, bloque = m.groups()
        lineas = [l[2:] for l in bloque.splitlines() if l.startswith("> ")]
        multi = "**Mensaje" in bloque
        prompts[pid] = {"id": pid, "titulo": re.sub(r"\s*\(.*\)$", "", titulo).strip(),
                        "mensajes": lineas if multi else ["\n".join(lineas)]}
    for m in re.finditer(r"- \*\*(P\d+|C1)[^*]*:\*\* (.+)", clave):
        pid, riesgo = m.groups()
        if pid in prompts:
            prompts[pid]["riesgo"] = re.sub(r"\*\*", "", riesgo).strip()
    for pid, p in prompts.items():
        p.update(area=AREA.get(pid, ""), dificultad=DIFICULTAD.get(pid, ""), resaltar=RESALTAR.get(pid, []))
    return prompts


def leer_respuestas():
    with (DATOS / "respuestas.csv").open(encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    out = []
    for r in filas:
        ruta = DATOS / "respuestas" / r["archivo"]
        if not ruta.exists():
            continue
        cuerpo = ruta.read_text(encoding="utf-8").split("\n---\n", 1)[-1].strip()
        captura = DATOS / "capturas" / r["archivo"].replace(".md", ".jpg")
        out.append({"app": r["app"], "prompt": r["prompt"], "tirada": int(r["tirada"]), "modelo": r["modelo"],
                    "sesion": r["sesion"], "fecha": f"{r['fecha']} {r['hora']}", "archivo": r["archivo"],
                    "captura": f"../datos/capturas/{captura.name}" if captura.exists() else None,
                    "notas": r.get("notas", ""), "texto": cuerpo})
    return out


def main():
    resultados, demo = None, False
    for carpeta, es_demo in (("resultados", False), ("resultados_demo", True)):
        ruta = RAIZ / carpeta / "resultados.json"
        if ruta.exists():
            resultados, demo = json.loads(ruta.read_text(encoding="utf-8")), es_demo
            break
    datos = {"prompts": leer_bateria(), "respuestas": leer_respuestas(),
             "resultados": resultados, "resultados_demo": demo}
    APP.mkdir(exist_ok=True)
    js = "window.DATOS = " + json.dumps(datos, ensure_ascii=False).replace("</", "<\\/") + ";\n"
    (APP / "data.js").write_text(js, encoding="utf-8")
    # Versión de un solo archivo (para mandarla o abrirla en cualquier navegador sin servidor)
    html = (APP / "index.html").read_text(encoding="utf-8")
    html = html.replace('<script src="data.js"></script>', "<script>" + js + "</script>")
    html = html.replace('href="${r.captura}"', 'href="${r.captura.replace(\'../\', \'\')}"')
    (RAIZ / "app_ia_avisa.html").write_text(html, encoding="utf-8")
    print(f"app/data.js: {len(datos['prompts'])} prompts, {len(datos['respuestas'])} respuestas, "
          f"resultados: {'DEMO' if demo else ('reales' if resultados else 'ninguno')}")


if __name__ == "__main__":
    main()
