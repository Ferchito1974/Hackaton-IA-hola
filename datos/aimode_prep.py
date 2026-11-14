import json, sys, hashlib, urllib.parse
from pathlib import Path
SP = Path(__file__).resolve().parent
name, sha, P = sys.argv[1:4]
t = json.loads((SP / f"{name}.json").read_text(encoding="utf-8")).strip()
h = hashlib.sha256(t.encode("utf-8")).hexdigest()
(SP / f"{name}.txt").write_bytes(t.encode("utf-8"))
print("len", len(t), "hash_ok", h == sha)
lines = Path(r"C:\Users\fereu\Desktop\Universidad\vision\hackathon_epistemics\piloto\bateria_prompts.md").read_text(encoding="utf-8").splitlines()
i = next(k for k, l in enumerate(lines) if l.startswith(f"## {P}."))
prompt = lines[i + 1][2:]
url = "https://www.google.com/search?hl=es&udm=50&q=" + urllib.parse.quote_plus(prompt, safe="") + "&csuir=1"
(SP / f"{name}.url").write_text(url, encoding="utf-8")
print("urllen", len(url))
