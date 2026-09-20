# -*- coding: utf-8 -*-
from pathlib import Path
import json, re

p = Path(r"C:\Users\jscjc\.local\share\mimocode\tool-output\tool_g001a0bf88cbca001GFonI9fO6")
raw = p.read_text(encoding="utf-8", errors="ignore")
data = json.loads(raw)
print("keys", data.keys())
print("season", data.get("season"), "version", data.get("version"), "n", len(data.get("data", [])))
# sample first items keys
for i, item in enumerate(data["data"][:5]):
    print(i, {k: item[k] for k in list(item)[:12]})
# find hero-like: maybe typeId for champions
types = {}
for item in data["data"]:
    types[item.get("typeId")] = types.get(item.get("typeId"), 0) + 1
print("typeId counts", types)
# search names that match our champions
want = ["阿卡丽","洛","慎","凯南","黛安娜","费德提克","拉克丝","卡兹克","约里克","沃里克","阿兹尔"]
for item in data["data"]:
    name = item.get("name","")
    if any(w in name for w in want):
        print("HIT", name, item.get("typeId"), item.get("imagePath","")[:80])
