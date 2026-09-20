# -*- coding: utf-8 -*-
"""Deeper search: can we reach 15+ non-unique traits?"""
from collections import defaultdict
import random

UNIQUE = {
    "Attuned", "Avatar", "Bounty Seeker", "Emerald Aspect", "Monolith",
    "Old Growth", "Thornmaiden", "Caustic", "Greenfather", "Apex Predator",
}
CN = {
    "Adaptor": "适应者", "Brawler": "斗士", "Defender": "守卫",
    "Executioner": "处刑者", "Hunter": "猎人", "Invoker": "唤魔者",
    "Juggernaut": "重装战士", "Rapidfire": "迅捷射手", "Ravager": "屠戮者",
    "Spellweaver": "织法者", "Summoner": "召唤使", "Vanguard": "先锋",
    "Blossom": "绽放", "Coven": "魔女", "Elderwood": "古林",
    "Blackthorn": "黑棘", "Fae": "花仙子", "Flora Fatalis": "致命花植",
    "Inferno": "炼狱", "Lunar": "月影", "Primal": "原始",
    "Riftbeast": "裂兽", "Solar": "日曜", "Sprykin": "灵捷",
    "Rival": "宿敌",
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
MAX_SLOTS = 11

def nu(n):
    return [t for t in U[n][1] if t not in UNIQUE]

def evaluate(units, lux, count_rival=True):
    slots = sum(U[n][2] for n in units) + (1 if lux else 0)
    if slots > MAX_SLOTS:
        return None
    if sum(1 for n in units if n in ("Kha'Zix", "Rengar")) > 1:
        return None
    c = defaultdict(int)
    for n in units:
        for t in U[n][1]:
            if t not in UNIQUE:
                c[t] += 1
        if n == "Elder Dragon":
            c["Riftbeast"] += 2
    if lux:
        c[LUX[lux]] += 2
    all_names = list(units) + ([lux] if lux else [])
    fae_ok = [n for n in all_names
              if not (n in LUX and LUX[n] == "Fae") and not (n in U and "Fae" in U[n][1])]
    coven_ok = [n for n in all_names
                if not (n in LUX and LUX[n] == "Coven") and not (n in U and "Coven" in U[n][1])]
    best_n, best_f, best_c, best_act, best_counts = -1, None, None, None, None
    for f in fae_ok:
        for cv in coven_ok:
            if f == cv:
                continue
            cc = defaultdict(int, c)
            cc["Fae"] += 1
            cc["Coven"] += 1
            act = [t for t, bp in BP.items() if cc[t] >= bp and (count_rival or t != "Rival")]
            if len(act) > best_n:
                best_n, best_f, best_c, best_act, best_counts = len(act), f, cv, act, cc
    if best_n < 0:
        cc = defaultdict(int, c)
        if fae_ok:
            cc["Fae"] += 1
        if coven_ok:
            cc["Coven"] += 1
        act = [t for t, bp in BP.items() if cc[t] >= bp and (count_rival or t != "Rival")]
        best_n, best_f, best_c, best_act, best_counts = len(act), fae_ok[0] if fae_ok else None, coven_ok[0] if coven_ok else None, act, cc
    return dict(n=best_n, units=list(units), lux=lux, slots=slots,
                fae=best_f, coven=best_c, act=best_act, counts=best_counts)

POOL = [n for n in U if nu(n) or n == "Elder Dragon"]

def local(res, count_rival=True):
    if not res:
        return res
    improved = True
    while improved:
        improved = False
        units, lux, cur_n = list(res["units"]), res["lux"], res["n"]
        opts = list(POOL) + list(LUX.keys())
        for rm in units + ([lux] if lux else []):
            for add in opts:
                if add == rm or add in units or add == lux:
                    continue
                tu, tl = list(units), lux
                if rm in LUX:
                    tl = None
                    tu = units
                else:
                    tu = [x for x in units if x != rm]
                if add in LUX:
                    if tl:
                        continue
                    tl = add
                else:
                    tu = tu + [add]
                r = evaluate(tu, tl, count_rival)
                if r and r["n"] > cur_n:
                    res, improved = r, True
                    break
            if improved:
                break
        if not improved and res["slots"] < MAX_SLOTS:
            for add in opts:
                if add in units or add == lux:
                    continue
                if add in LUX and lux:
                    continue
                sc = 1 if add in LUX else U[add][2]
                if res["slots"] + sc > MAX_SLOTS:
                    continue
                r = evaluate(units + ([add] if add not in LUX else []), add if add in LUX else lux, count_rival)
                if r and r["n"] > cur_n:
                    res, improved = r, True
                    break
        if not improved:
            for rm in units + ([lux] if lux else []):
                if rm in LUX:
                    r = evaluate(units, None, count_rival)
                else:
                    r = evaluate([x for x in units if x != rm], lux, count_rival)
                if r and r["n"] > cur_n:
                    res, improved = r, True
                    break
    return res

best = None
best_no_rival = None

def consider(r, use_rival=True):
    global best, best_no_rival
    if not r:
        return
    if use_rival:
        if best is None or r["n"] > best["n"]:
            best = r
            print(f"[Rival+] {r['n']}: {r['units']} lux={r['lux']} fae={r['fae']} coven={r['coven']}")
            print(f"   {sorted(r['act'])}")
    else:
        if best_no_rival is None or r["n"] > best_no_rival["n"]:
            best_no_rival = r
            print(f"[Rival-] {r['n']}: {r['units']} lux={r['lux']} fae={r['fae']} coven={r['coven']}")
            print(f"   {sorted(r['act'])}")

# Seed from known good
seeds = [
    ["Rakan", "Yorick", "Shen", "Warwick", "Azir", "Diana", "Fiddlesticks", "Kha'Zix", "Alune", "Kennen"],
    ["Rakan", "Yorick", "Shen", "Warwick", "Azir", "Diana", "Fiddlesticks", "Kha'Zix", "Kennen", "Morgana"],
    ["Akali", "Rakan", "Shen", "Diana", "Fiddlesticks", "Vi", "Nidalee", "Alune", "Elder Dragon", "Kennen"],
    ["Rakan", "Xayah", "Tristana", "Lillia", "Caitlyn", "Elise", "Fiddlesticks", "Soraka", "Yunara", "Morgana", "Camille"],
    ["Akali", "Varus", "Shen", "Kennen", "Amumu", "Camille", "Murkwolf", "Warwick", "Diana", "Fiddlesticks", "Rakan"],
    ["Rakan", "Yorick", "Karma", "Yunara", "Ahri", "Sett", "Kobuko", "Tristana", "Caitlyn", "Fiddlesticks", "Soraka"],
    ["Xayah", "Rakan", "Kayle", "Leona", "Sejuani", "Ornn", "Alistar", "Ezreal", "Gnar", "Hecarim", "LeBlanc"],
    ["Rakan", "Tristana", "Lillia", "Xayah", "Vi", "Nidalee", "Sivir", "Kog'Maw", "Gromp", "Master Yi", "Teemo"],
    ["Caitlyn", "Camille", "Elise", "Cassiopeia", "Morgana", "Rakan", "Yunara", "Fiddlesticks", "Soraka", "Yorick", "Karma"],
    ["Akali", "Shen", "Kennen", "Varus", "Amumu", "Rakan", "Diana", "Warwick", "Azir", "Fiddlesticks", "Kha'Zix"],
    ["Rakan", "Xayah", "Diana", "Aphelios", "Alune", "Kayle", "Leona", "Sejuani", "Fiddlesticks", "Soraka", "Tristana"],
    ["Akali", "Gromp", "Kog'Maw", "Master Yi", "Nidalee", "Rakan", "Vi", "Veigar", "Warwick", "Fiddlesticks", "Kha'Zix"],
    ["Rakan", "Yorick", "Azir", "Mama Beak", "Zyra", "Caitlyn", "Sivir", "Ashe", "Fiddlesticks", "Soraka", "Kennen"],
    ["Pebbles", "Teemo", "Kog'Maw", "Sentinel", "Morgana", "Rakan", "Diana", "Hecarim", "Fiddlesticks", "Akali", "Kha'Zix"],
    ["Kobuko", "Rek'Sai", "Alistar", "Krug", "Sett", "Gnar", "Rakan", "Yorick", "Tristana", "Fiddlesticks", "Camille"],
    ["Leona", "Ornn", "Shen", "Fiddlesticks", "Rammus", "Lillia", "Rakan", "Diana", "Warwick", "Azir", "Kha'Zix"],
    ["Cinderling", "Caitlyn", "Tristana", "Sivir", "Ashe", "Rakan", "Yorick", "Fiddlesticks", "Soraka", "Camille", "Karma"],
    ["Varus", "Xayah", "Kayle", "Mama Beak", "Aphelios", "Rakan", "Diana", "Fiddlesticks", "Alune", "Kennen", "Yorick"],
    ["Akali", "Camille", "Murkwolf", "Warwick", "Diana", "Brambleback", "Rakan", "Shen", "Fiddlesticks", "Azir", "Kha'Zix"],
    ["Karma", "Veigar", "LeBlanc", "Cassiopeia", "Fiddlesticks", "Ahri", "Alune", "Rakan", "Yorick", "Diana", "Kennen"],
]

for team in seeds:
    if sum(U[n][2] for n in team) > MAX_SLOTS:
        # try without elder dragon style overflow
        team = [n for n in team if n != "Elder Dragon"][:11]
        if sum(U[n][2] for n in team) > MAX_SLOTS:
            continue
    for lux in [None] + list(LUX.keys()):
        r = evaluate(team, lux, True)
        consider(r, True)
        if r:
            r2 = local(evaluate(team, lux, True), True)
            consider(r2, True)
        r = evaluate(team, lux, False)
        consider(r, False)
        if r:
            r2 = local(evaluate(team, lux, False), False)
            consider(r2, False)

# Random restarts with pair-completion heuristic
random.seed(7)
for restart in range(800):
    team = []
    slots = 0
    counts = defaultdict(int)
    # Prefer 3-trait non-unique units
    weights = {n: len(nu(n)) + (2 if n == "Elder Dragon" else 0) for n in POOL}
    names = list(POOL)
    wts = [weights[n] for n in names]
    # start with random 2-trait connector
    start = random.choices(names, weights=wts, k=1)[0]
    team.append(start)
    slots = U[start][2]
    for t in nu(start):
        counts[t] += 1
    if start == "Elder Dragon":
        counts["Riftbeast"] += 2
    while slots < MAX_SLOTS:
        pick = None
        bestg = -99
        for n in names:
            if n in team:
                continue
            if n in ("Kha'Zix", "Rengar") and any(x in ("Kha'Zix", "Rengar") for x in team):
                continue
            if slots + U[n][2] > MAX_SLOTS:
                continue
            g = 0
            tr = defaultdict(int, counts)
            for t in nu(n):
                tr[t] += 1
            if n == "Elder Dragon":
                tr["Riftbeast"] += 2
            for t, bp in BP.items():
                if counts[t] < bp <= tr[t]:
                    g += 4
                elif counts[t] < bp and tr[t] > counts[t]:
                    # progress toward BP
                    g += 0.5
            g += 0.15 * len(nu(n))
            g += random.random() * 0.3
            if g > bestg:
                bestg, pick = g, n
        if pick is None:
            break
        team.append(pick)
        slots += U[pick][2]
        for t in nu(pick):
            counts[t] += 1
        if pick == "Elder Dragon":
            counts["Riftbeast"] += 2
    for lux in [None] + list(LUX.keys()):
        consider(evaluate(team, lux, True), True)
        consider(evaluate(team, lux, False), False)

# Polish
if best:
    best = local(best, True)
if best_no_rival:
    best_no_rival = local(best_no_rival, False)

# Pair-complete exhaustive: choose activated trait set of size 14-16 and check feasibility
print("\n--- Feasibility probe for 15 traits ---")
# Try replacing Kha'Zix with various units in best team, or swap two units
if best:
    base_units = [u for u in best["units"]]
    base_lux = best["lux"]
    for drop_i in range(len(base_units)):
        for add1 in POOL:
            if add1 in base_units:
                continue
            tu = [u for j, u in enumerate(base_units) if j != drop_i] + [add1]
            if sum(U[n][2] for n in tu) + (1 if base_lux else 0) > MAX_SLOTS:
                continue
            for lux in [None] + list(LUX.keys()):
                r = evaluate(tu, lux, True)
                if r:
                    consider(r, True)
                    if r["n"] >= 15:
                        r = local(r, True)
                        consider(r, True)
                r = evaluate(tu, lux, False)
                if r:
                    consider(r, False)

# Double swap from best
if best:
    units0 = list(best["units"])
    lux0 = best["lux"]
    for i in range(len(units0)):
        for j in range(i + 1, len(units0)):
            for a in POOL:
                if a in units0:
                    continue
                for b in POOL:
                    if b in units0 or b == a:
                        continue
                    tu = list(units0)
                    tu[i], tu[j] = a, b
                    if sum(U[n][2] for n in tu) + (1 if lux0 else 0) > MAX_SLOTS:
                        continue
                    r = evaluate(tu, lux0, True)
                    if r and r["n"] >= (best["n"] if best else 0):
                        consider(local(r, True) if r["n"] >= 14 else r, True)
                    r = evaluate(tu, lux0, False)
                    if r and best_no_rival and r["n"] >= best_no_rival["n"]:
                        consider(local(r, False) if r["n"] >= 13 else r, False)

print("\n" + "=" * 60)
print("BEST (Rival counted):", best["n"] if best else None)
if best:
    print(" units:", best["units"])
    print(" lux:", best["lux"], "emblems:", best["fae"], best["coven"], "slots", best["slots"])
    print(" activated:", sorted(best["act"]))
    for t in sorted(best["act"], key=lambda x: (-best["counts"][x], x)):
        print(f"   {t}/{CN.get(t,t)} {best['counts'][t]}/{BP[t]}")

print("\nBEST (Rival NOT counted):", best_no_rival["n"] if best_no_rival else None)
if best_no_rival:
    print(" units:", best_no_rival["units"])
    print(" lux:", best_no_rival["lux"], "emblems:", best_no_rival["fae"], best_no_rival["coven"], "slots", best_no_rival["slots"])
    print(" activated:", sorted(best_no_rival["act"]))
    for t in sorted(best_no_rival["act"], key=lambda x: (-best_no_rival["counts"][x], x)):
        print(f"   {t}/{CN.get(t,t)} {best_no_rival['counts'][t]}/{BP[t]}")
