# -*- coding: utf-8 -*-
from pathlib import Path
import json

p = Path(r"C:\Users\jscjc\.local\share\mimocode\tool-output\tool_g001a0bf8958ac001sYWrA1bB9")
raw = p.read_text(encoding="utf-8", errors="ignore")
print(raw[:200])
data = json.loads(raw)
print("keys", data.keys() if isinstance(data, dict) else type(data))
if isinstance(data, dict):
    print("season", data.get("season"), "n", len(data.get("data", [])))
    items = data["data"]
    print("sample keys", items[0].keys())
    for it in items[:3]:
        print({k: it[k] for k in list(it)[:15]})
    # look for our units
    want_en = ["Akali","Rakan","Pebbles","Fiddlesticks","Lux","Kennen","Kha","Yorick"]
    for it in items:
        name = str(it.get("name","")) + str(it.get("displayName","")) + str(it.get("title",""))
        en = str(it.get("englishName","")) + str(it.get("alias","")) + str(it.get("chessId","")) + str(it.get("heroId",""))
        if any(w.lower() in (name+en).lower() for w in ["阿卡丽","洛","慎","凯南","拉克丝","卡兹克","约里克","费德提克","卵石","余烬"]):
            print("CN", it.get("name"), it.get("title"), it.get("imagePath") or it.get("icon") or list(it.items())[:8])
