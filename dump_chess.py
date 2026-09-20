# -*- coding: utf-8 -*-
from pathlib import Path
import json

chess = json.loads(Path(r"C:\Users\jscjc\.local\share\mimocode\tool-output\tool_g001a0bf8958ac001sYWrA1bB9").read_text(encoding="utf-8"))
# race/job already known from previous fetch - re-fetch inline from saved? parse race/job from web files if needed
# extract champions
rows = []
for it in chess["data"]:
    if str(it.get("price","0")) in ("0","None","") and it.get("displayName") in ("沙兵","深林守卫"):
        continue
    # keep playable with price>0 or lux forms
    en = it.get("hero_EN_name") or ""
    img = it.get("json_chess_image_url") or it.get("originalImage") or ""
    skill = it.get("skillImage") or ""
    rows.append({
        "id": it.get("chessId"),
        "cn": it.get("displayName"),
        "en": en,
        "price": it.get("price"),
        "races": it.get("raceIds"),
        "jobs": it.get("jobIds"),
        "img": img,
        "skillImage": skill,
        "synergies": it.get("synergies"),
    })

for r in rows:
    if r["price"] and r["price"] != "0":
        print(f"{r['price']}\t{r['cn']}\t{r['en']}\t{r['races']}\t{r['jobs']}\t{r['img'][:90]}")

print("TOTAL", len(rows), "playable", sum(1 for r in rows if r['price'] not in ('0',None,'')))
# sample images
print("IMG samples:")
for r in rows[:8]:
    print(r["cn"], r["img"], r["skillImage"][:80] if r["skillImage"] else "")
