"""Lista las respuestas en las que los dos evaluadores no coinciden, para resolverlas juntos.

Crea clasificacion/consenso.csv con una fila por desacuerdo: lo que puso cada evaluador y
columnas vacías para la decisión común (mismo formato que las hojas de evaluador). Las filas
que dejen vacías se ignoran y se usa el evaluador 1. No dice qué app es cada respuesta.

Uso: python datos/preparar_consenso.py   (no sobrescribe un consenso.csv ya existente)
"""
import csv
from pathlib import Path

CLAS = Path(__file__).resolve().parent.parent / "clasificacion"
COLS = ["avisa (si/debil/no)", "plan_seguro (si/no)", "falsa_seguridad (si/no)"]


def leer(n):
    with (CLAS / f"evaluador{n}.csv").open(encoding="utf-8-sig") as f:
        return {r["codigo"]: r for r in csv.DictReader(f)}


def norm(v):
    return (v or "").strip().lower()


def main():
    destino = CLAS / "consenso.csv"
    if destino.exists():
        raise SystemExit("consenso.csv ya existe: no se sobrescribe.")
    e1, e2 = leer(1), leer(2)
    filas = []
    for c in sorted(e1, key=lambda c: (e1[c]["prompt"], c)):
        dif = [col for col in COLS if norm(e1[c][col]) != norm(e2[c][col])]
        if dif:
            filas.append({"codigo": c, "prompt": e1[c]["prompt"],
                          "en_desacuerdo": " | ".join(d.split(" (")[0] for d in dif),
                          **{f"ev1 {col.split(' (')[0]}": e1[c][col] for col in COLS},
                          **{f"ev2 {col.split(' (')[0]}": e2[c][col] for col in COLS},
                          "notas ev1": e1[c].get("notas", ""), "notas ev2": e2[c].get("notas", ""),
                          **{col: "" for col in COLS}, "notas": ""})
    with destino.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} desacuerdos en {destino}")


if __name__ == "__main__":
    main()
