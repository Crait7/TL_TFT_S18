# -*- coding: utf-8 -*-
from pathlib import Path
import json, re

data = json.loads(Path(r"C:\Users\jscjc\.local\share\mimocode\tool-output\tool_g001a0bf9009b6001JTiXLE0op").read_text(encoding="utf-8"))

# hero keys
for h in data["heros18"][:8]:
    print(h.get("displayName"), "key=", h.get("key"), "code=", h.get("code"),
          "tftCode=", h.get("tftCode"), "chessId=", h.get("chessId"),
          "enTraits=", h.get("enTraits"), "jobs=", h.get("jobs"), "races=", h.get("races"))

print("\n--- all keys ---")
for h in data["heros18"]:
    print(f"{h.get('displayName')}\t{h.get('key')}\t{h.get('code')}\t{h.get('tftCode')}\t{h.get('chessId')}\t{h.get('namePinyin')}")

print("\n--- h5TraitIcons sample ---")
icons = data.get("h5TraitIcons") or {}
for i, (k,v) in enumerate(list(icons.items())[:8]):
    print(k, v)

print("\n--- races/jobs ---")
for r in data.get("races18", [])[:5]:
    print(r if not isinstance(r, dict) else {k:r[k] for k in list(r)[:8]})
for j in data.get("jobs18", [])[:5]:
    print(j if not isinstance(j, dict) else {k:j[k] for k in list(j)[:8]})
