import sys, subprocess, csv
from pathlib import Path
D = Path(r"C:\Users\fereu\Desktop\Universidad\vision\hackathon_epistemics\datos")
tf, model, prompt, run, explen, exph = sys.argv[1:7]
url = "https://claude.ai/new?incognito (chat incógnito, sin URL propia)"
txt = Path(tf).read_text(encoding='utf-8')
if tf.endswith('.json'): import json; txt = json.loads(txt.strip())
if txt.endswith('\n'): txt = txt[:-1]
if len(txt) != int(explen):
    sys.exit(f"LENGTH MISMATCH file={len(txt)} expected={explen}")
h = 0
for ch in txt: h = (h*31+ord(ch)) % 1000000007
if h != int(exph): sys.exit(f"HASH MISMATCH {h} vs {exph}")
r = subprocess.run([sys.executable, "guardar.py", "claude", model, prompt, run, url], input=txt.encode('utf-8'), cwd=D, capture_output=True)
print(r.stdout.decode('utf-8', 'replace'), r.stderr.decode('utf-8', 'replace'))
if r.returncode != 0: sys.exit(1)
name = f"claude_{prompt}_t{run}.md"
md = D / "respuestas" / name
lines = md.read_text(encoding='utf-8').split('\n')
assert "Sin sesión" in lines[0]
lines[0] = lines[0].replace("Sin sesión", "Segunda cuenta gratuita, chat incógnito", 1)
md.write_text('\n'.join(lines), encoding='utf-8')
c = D / "respuestas.csv"
raw = c.read_bytes(); bom = raw.startswith(b'\xef\xbb\xbf')
with c.open(encoding='utf-8-sig', newline='') as f: rows = list(csv.reader(f))
n = 0
for row in rows:
    if len(row) > 8 and row[8] == name and row[5] == "sin":
        row[5] = "cuenta 2"; n += 1
assert n == 1, n
with c.open('w', encoding='utf-8-sig' if bom else 'utf-8', newline='') as f: csv.writer(f).writerows(rows)
body = md.read_text(encoding='utf-8').split("\n\n---\n\n", 1)[1].rstrip('\n')
print("fixed; body chars", len(body), "match" if body == txt.strip() else "BODY DIFFERS")
