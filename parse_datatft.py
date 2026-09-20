# -*- coding: utf-8 -*-
from pathlib import Path
import json, re

p = Path(r"C:\Users\jscjc\.local\share\mimocode\tool-output\tool_g001a0bf9009b6001JTiXLE0op")
raw = p.read_text(encoding="utf-8", errors="ignore")
print("len", len(raw))
print(raw[:300])

# find image url patterns
urls = re.findall(r'https?://[^"\\ ]+\.(?:png|jpg|jpeg|webp)', raw)
print("url count", len(urls))
print("samples", urls[:20])
# unique domains
doms = {}
for u in urls:
    d = u.split("/")[2]
    doms[d] = doms.get(d, 0) + 1
print("domains", sorted(doms.items(), key=lambda x: -x[1])[:10])

# parse json if possible
try:
    data = json.loads(raw)
    print("type", type(data), list(data)[:20] if isinstance(data, dict) else "list")
    if isinstance(data, dict):
        for k in data:
            v = data[k]
            print(k, type(v), (len(v) if hasattr(v, "__len__") else v) if not isinstance(v, (dict,)) else list(v)[:8])
except Exception as e:
    print("json err", e)
    # try find champion-like keys
    for m in re.finditer(r'"(?:name|championName|unit|hero)"\s*:\s*"([^"]{2,20})"', raw[:50000]):
        print("name", m.group(1))
