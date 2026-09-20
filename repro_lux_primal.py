# -*- coding: utf-8 -*-
"""Reproduce: 11 slots, no emblems — does search miss Lux activating BP=2 origins alone?"""
from collections import defaultdict

UNIQUE = {
    "Attuned", "Avatar", "Bounty Seeker", "Emerald Aspect", "Monolith",
    "Old Growth", "Thornmaiden", "Caustic", "Greenfather", "Apex Predator",
}
BP = {
    "Adaptor": 2, "Brawler": 2, "Defender": 2, "Executioner": 2,
    "Hunter": 2, "Invoker": 2, "Juggernaut": 2, "Rapidfire": 2,
    "Ravager": 2, "Spellweaver": 2, "Summoner": 2, "Vanguard": 2,
    "Blossom": 3, "Coven": 3, "Elderwood": 3, "Blackthorn": 2,
    "Fae": 2, "Flora Fatalis": 1, "Inferno": 2, "Lunar": 2,
    "Primal": 2, "Riftbeast": 3, "Solar": 3, "Sprykin": 3,
    "Rival": 1,
}
U = {
    "Akali": (1, ["Inferno", "Adaptor", "Ravager"], 1),
    "Camille": (1, ["Coven", "Ravager"], 1),
    "Cinderling": (1, ["Riftbeast", "Hunter"], 1),
    "Karma": (1, ["Blossom", "Spellweaver"], 1),
    "Kobuko": (1, ["Sprykin", "Brawler"], 1),
    "Leona": (1, ["Solar", "Defender"], 1),
    "Ornn": (1, ["Elderwood", "Defender"], 1),
    "Pebbles": (1, ["Riftbeast", "Invoker"], 1),
    "Rakan": (1, ["Fae", "Juggernaut", "Vanguard"], 1),
    "Rek'Sai": (1, ["Blackthorn", "Brawler"], 1),
    "Varus": (1, ["Inferno", "Rapidfire"], 1),
    "Veigar": (1, ["Blackthorn", "Sprykin", "Spellweaver"], 1),
    "Xayah": (1, ["Elderwood", "Fae", "Rapidfire"], 1),
    "Yorick": (1, ["Blossom", "Juggernaut", "Summoner"], 1),
    "Alistar": (2, ["Elderwood", "Brawler"], 1),
    "Caitlyn": (2, ["Coven", "Hunter"], 1),
    "Elise": (2, ["Coven", "Vanguard"], 1),
    "Gromp": (2, ["Riftbeast", "Adaptor"], 1),
    "Kayle": (2, ["Solar", "Rapidfire"], 1),
    "LeBlanc": (2, ["Elderwood", "Spellweaver"], 1),
    "Murkwolf": (2, ["Riftbeast", "Ravager"], 1),
    "Scuttlecrab": (2, ["Riftbeast", "Juggernaut"], 1),
    "Sejuani": (2, ["Solar", "Juggernaut"], 1),
    "Shen": (2, ["Inferno", "Defender"], 1),
    "Teemo": (2, ["Sprykin", "Invoker"], 1),
    "Warwick": (2, ["Blackthorn", "Ravager"], 1),
    "Yunara": (2, ["Blossom", "Executioner"], 1),
    "Azir": (3, ["Blackthorn", "Executioner", "Summoner"], 1),
    "Cassiopeia": (3, ["Coven", "Spellweaver"], 1),
    "Diana": (3, ["Lunar", "Ravager", "Vanguard"], 1),
    "Fiddlesticks": (3, ["Flora Fatalis", "Defender", "Spellweaver"], 1),
    "Hecarim": (3, ["Elderwood", "Vanguard"], 1),
    "Kha'Zix": (3, ["Rival"], 1),
    "Kog'Maw": (3, ["Caustic", "Invoker", "Adaptor"], 1),
    "Krug": (3, ["Riftbeast", "Brawler"], 1),
    "Master Yi": (3, ["Blossom", "Adaptor"], 1),
    "Rammus": (3, ["Sprykin", "Defender"], 1),
    "Mama Beak": (3, ["Riftbeast", "Summoner", "Rapidfire"], 1),
    "Rengar": (3, ["Rival"], 1),
    "Tristana": (3, ["Fae", "Sprykin", "Hunter"], 1),
    "Vi": (3, ["Primal", "Juggernaut"], 1),
    "Ahri": (4, ["Blossom", "Spellweaver"], 1),
    "Amumu": (4, ["Inferno", "Juggernaut"], 1),
    "Sentinel": (4, ["Riftbeast", "Vanguard", "Invoker"], 1),
    "Aphelios": (4, ["Lunar", "Rapidfire"], 1),
    "Brambleback": (4, ["Riftbeast", "Ravager"], 1),
    "Ezreal": (4, ["Elderwood", "Executioner"], 1),
    "Lillia": (4, ["Fae", "Defender"], 1),
    "Malphite": (4, ["Blackthorn", "Monolith"], 1),
    "Morgana": (4, ["Coven", "Invoker"], 1),
    "Nidalee": (4, ["Primal", "Adaptor"], 1),
    "Sett": (4, ["Blossom", "Brawler"], 1),
    "Sivir": (4, ["Primal", "Hunter"], 1),
    "Soraka": (4, ["Flora Fatalis", "Executioner"], 1),
    "Zyra": (4, ["Thornmaiden", "Summoner"], 1),
    "Alune": (5, ["Attuned", "Lunar", "Spellweaver"], 1),
    "Ashe": (5, ["Blossom", "Hunter"], 1),
    "Draven": (5, ["Bounty Seeker"], 1),
    "Elder Dragon": (5, ["Riftbeast", "Apex Predator"], 2),
    "Gnar": (5, ["Elderwood", "Sprykin", "Brawler"], 1),
    "Ivern": (5, ["Greenfather"], 1),
    "Kennen": (5, ["Inferno", "Executioner"], 1),
    "Maokai": (5, ["Old Growth", "Juggernaut"], 1),
    "Taric": (5, ["Emerald Aspect", "Vanguard"], 1),
}
LUX = {
    "Lux Fae": "Fae", "Lux Coven": "Coven", "Lux Solar": "Solar",
    "Lux Primal": "Primal", "Lux Blackthorn": "Blackthorn",
    "Lux Blossom": "Blossom", "Lux Inferno": "Inferno",
    "Lux Elderwood": "Elderwood", "Lux Lunar": "Lunar",
}

def nu(n):
    return [t for t in U[n][1] if t not in UNIQUE]

def counts_for(units, lux=None, lux_double=True):
    c = defaultdict(int)
    for n in units:
        for t in U[n][1]:
            if t not in UNIQUE:
                c[t] += 1
        if n == "Elder Dragon":
            c["Riftbeast"] += 2
    if lux:
        c[LUX[lux]] += 2 if lux_double else 1
    return c

def activated(c):
    return sorted([t for t, bp in BP.items() if c[t] >= bp])

# Known good 10-slot cores without lux
core = ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir",
        "Veigar", "Diana", "Aphelios", "Akali", "Kennen"]
print("=== 10人口无拉克丝 ===")
c10 = counts_for(core)
a10 = activated(c10)
print("n=", len(a10), a10)
print("Primal", c10["Primal"], "Fae", c10["Fae"], "Blackthorn", c10["Blackthorn"],
      "Inferno", c10["Inferno"], "Lunar", c10["Lunar"])

print("\n=== 同10人 + 各形态拉克丝（双计）第11人口 ===")
for lx, origin in LUX.items():
    c = counts_for(core, lx, True)
    a = activated(c)
    delta = set(a) - set(a10)
    print(f"{lx:16} {origin:12} count={c[origin]:2}  n={len(a):2}  new={sorted(delta) or '—'}")

print("\n=== 关键规则 ===")
print("Avatar 双计下，拉克丝单独可点亮门槛=2 的源系：")
for lx, origin in LUX.items():
    bp = BP[origin]
    alone = 2  # double count
    print(f"  {lx}: {origin} +2 → {alone}/{bp} {'激活' if alone>=bp else '不足'}")

# What if we wrongly pick Lux Coven (BP3)?
print("\n=== 错误示范：塞 Lux Coven/Solar/Blossom/Elderwood（门槛3，+2不够）===")
for bad in ["Lux Coven", "Lux Solar", "Lux Blossom", "Lux Elderwood"]:
    c = counts_for(core, bad, True)
    a = activated(c)
    print(f"{bad}: n={len(a)} vs 10人口 n={len(a10)}  差额={len(a)-len(a10)}")

print("\n=== 正确示范：塞能单独点亮的形态 ===")
for good in ["Lux Primal", "Lux Fae", "Lux Blackthorn", "Lux Inferno", "Lux Lunar"]:
    c = counts_for(core, good, True)
    a = activated(c)
    print(f"{good}: n={len(a)} new={sorted(set(a)-set(a10))}")
