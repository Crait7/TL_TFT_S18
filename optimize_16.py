# -*- coding: utf-8 -*-
"""Try to push past 15: base 14 + 2 emblem finishes, or base 13+2 with Lux."""
from collections import defaultdict
import random
import itertools

# reuse data by exec
import runpy
# inline data - import from previous by redefining quickly
exec(open(r"E:\mimo\projects\.mimo-sessions\2026-09-20\帮我调研现版本云顶之奕棋子的羁绊分布情况，在最多10个棋子+1个花仙子转职的情况\optimize_any_emblem.py", encoding="utf-8").read().split("POOL =")[0])

POOL = [n for n in U if nu(n) or n == "Elder Dragon"]
best = None

def evaluate(units, lux):
    return __import__("importlib").import_module  # placeholder

# re-define evaluate from file logic
def native_set(name):
    if name in LUX:
        return {LUX[name]}
    return set(U[name][1])

def evaluate(units, lux):
    slots = sum(U[n][2] for n in units) + (1 if lux else 0)
    if slots > MAX_SLOTS:
        return None
    if sum(1 for n in units if n in ("Kha'Zix", "Rengar")) > 1:
        return None
    counts = defaultdict(int)
    for n in units:
        for t in U[n][1]:
            if t not in UNIQUE:
                counts[t] += 1
        if n == "Elder Dragon":
            counts["Riftbeast"] += 2
    if lux:
        counts[LUX[lux]] += 2
    board = list(units) + ([lux] if lux else [])
    native = {n: native_set(n) for n in board}
    already = set()
    finish1 = []
    finish2 = []
    for t, bp in BP.items():
        c = counts[t]
        if c >= bp:
            already.add(t)
        elif bp - c == 1:
            elig = [u for u in board if t not in native[u]]
            if elig:
                finish1.append((t, elig))
        elif bp - c == 2:
            elig = [u for u in board if t not in native[u]]
            if len(elig) >= 2:
                finish2.append((t, elig))
    best_add = set()
    best_em = (None, None)
    for (t1, e1), (t2, e2) in itertools.combinations(finish1, 2):
        if t1 == t2:
            continue
        for u1 in e1:
            for u2 in e2:
                if u1 != u2:
                    best_add = {t1, t2}
                    best_em = ((u1, t1), (u2, t2))
                    break
            if len(best_add) == 2:
                break
        if len(best_add) == 2:
            break
    if len(best_add) < 2 and finish1:
        t, e = finish1[0]
        # find second
        best_add = {t}
        best_em = ((e[0], t), None)
        for t2, e2 in finish1:
            if t2 == t:
                continue
            for u2 in e2:
                if u2 != e[0]:
                    best_add = {t, t2}
                    best_em = ((e[0], t), (u2, t2))
                    break
            if len(best_add) == 2:
                break
    if len(best_add) < 1 and finish2:
        t, e = finish2[0]
        best_add = {t}
        best_em = ((e[0], t), (e[1], t))
    act = already | best_add
    final_c = defaultdict(int, counts)
    if best_em[0]:
        final_c[best_em[0][1]] += 1
    if best_em[1]:
        final_c[best_em[1][1]] += 1
    return dict(n=len(act), units=list(units), lux=lux, slots=slots,
                em1=best_em[0], em2=best_em[1], act=sorted(act), counts=dict(final_c),
                base=sorted(already), add=sorted(best_add),
                finish1=[t for t,_ in finish1], finish2=[t for t,_ in finish2],
                base_n=len(already))

def consider(r):
    global best
    if not r:
        return
    if best is None or r["n"] > best["n"]:
        best = r
        print(f"BEST {r['n']} base={r['base_n']}+{r['add']} lux={r['lux']}")
        print(f"  {r['units']}")
        print(f"  em={r['em1']}|{r['em2']}")
        print(f"  finish1={r['finish1']}")
        print(f"  ACT={r['act']}")

# Targeted constructions for base 14 + 2 finish1 (BP3 at 2)
# Pattern: Rival + FF + many BP2 pairs + two BP3 leftovers at 2

manual = [
    # 3 Riftbeast + FF + Rival + pairs, try leave Sprykin/Blossom/Coven at 2
    ["Pebbles", "Sentinel", "Mama Beak", "Fiddlesticks", "Kha'Zix", "Veigar",
     "Tristana", "Kobuko", "Gnar", "Rammus", "Teemo"],  # Sprykin path
    ["Pebbles", "Sentinel", "Mama Beak", "Fiddlesticks", "Kha'Zix", "Karma",
     "Yorick", "Yunara", "Ahri", "Sett", "Ashe"],  # Blossom path
    ["Camille", "Caitlyn", "Elise", "Fiddlesticks", "Kha'Zix", "Rakan",
     "Yorick", "Shen", "Warwick", "Azir", "Diana"],
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
     "Diana", "Aphelios", "Akali", "Kennen", "Lillia"],  # known 15
    # swap Lillia out, add unit that creates second finish1
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
     "Diana", "Aphelios", "Akali", "Kennen", "Rakan"],
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
     "Diana", "Aphelios", "Akali", "Kennen", "Yorick"],
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
     "Diana", "Aphelios", "Akali", "Kennen", "Kha'Zix"],
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
     "Diana", "Aphelios", "Akali", "Kennen", "Camille"],
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
     "Diana", "Aphelios", "Akali", "Kennen", "MasterYi" if False else "Master Yi"],
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
     "Diana", "Aphelios", "Akali", "Kennen", "Gromp"],
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
     "Diana", "Aphelios", "Akali", "Kennen", "Nidalee"],
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
     "Diana", "Aphelios", "Akali", "Kennen", "Vi"],
    # Elderwood at 2 leftovers
    ["Ornn", "Xayah", "Hecarim", "Fiddlesticks", "Kha'Zix", "Leona",
     "Kayle", "Sejuani", "Rakan", "Diana", "Kennen"],
    ["Ornn", "Alistar", "LeBlanc", "Fiddlesticks", "Karma", "Ahri",
     "Yorick", "Yunara", "Ashe", "Sett", "Master Yi"],
    # maximize finish1 pairs: board with many traits at exactly 1
    ["Akali", "Rakan", "Yorick", "Shen", "Warwick", "Azir", "Diana",
     "Fiddlesticks", "Kennen", "Camille", "Karma"],
    ["Akali", "Gromp", "Kog'Maw", "Master Yi", "Rakan", "Yorick",
     "Fiddlesticks", "Kennen", "Diana", "Vi", "Teemo"],
    ["Caitlyn", "Cinderling", "Tristana", "Sivir", "Ashe", "Rakan",
     "Yorick", "Fiddlesticks", "Soraka", "Karma", "Yunara"],
    ["Varus", "Xayah", "Kayle", "Aphelios", "Rakan", "Diana",
     "Fiddlesticks", "Alune", "Kennen", "Yorick", "Mama Beak"],
    ["Camille", "Warwick", "Murkwolf", "Akali", "Diana", "Brambleback",
     "Rakan", "Yorick", "Shen", "Fiddlesticks", "Kennen"],
    ["Veigar", "Rek'Sai", "Warwick", "Azir", "Rakan", "Yorick",
     "Fiddlesticks", "Karma", "Alune", "Diana", "Camille"],
    ["Kobuko", "Rammus", "Teemo", "Veigar", "Tristana", "Gnar",
     "Sett", "Krug", "Alistar", "Fiddlesticks", "Rakan"],
    ["Yorick", "Karma", "Yunara", "Ahri", "Ashe", "Sett", "Master Yi",
     "Azir", "Mama Beak", "Zyra", "Fiddlesticks"],
    ["Pebbles", "Teemo", "Sentinel", "Morgana", "Kog'Maw", "Rakan",
     "Yorick", "Fiddlesticks", "Akali", "Diana", "Kennen"],
    ["Cinderling", "Gromp", "Murkwolf", "Scuttlecrab", "Krug", "Mama Beak",
     "Pebbles", "Sentinel", "Brambleback", "Akali", "Kennen"],
    ["Leona", "Kayle", "Sejuani", "Ornn", "Alistar", "Ezreal", "Gnar",
     "LeBlanc", "Hecarim", "Xayah", "Rakan"],
    ["Camille", "Caitlyn", "Elise", "Cassiopeia", "Morgana", "Yunara",
     "Soraka", "Fiddlesticks", "Karma", "Ahri", "Rakan"],
]

print("Manual targeted...")
for team in manual:
    if sum(U[n][2] for n in team) > MAX_SLOTS:
        print(" skip slots", team, sum(U[n][2] for n in team))
        continue
    for lux in [None] + list(LUX.keys()):
        consider(evaluate(team, lux))

# Mutate known 15 board
base15 = ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar",
          "Diana", "Aphelios", "Akali", "Kennen", "Lillia"]
print("Mutate 15-board...")
for i in range(len(base15)):
    for a in POOL + list(LUX.keys()):
        if a in base15:
            continue
        if a in LUX:
            tu = [base15[j] for j in range(len(base15)) if j != i]
            r = evaluate(tu, a)
        else:
            tu = list(base15)
            tu[i] = a
            r = evaluate(tu, None)
        if r:
            consider(r)
            # also try lux variants on mutated
            if a not in LUX:
                for lx in LUX:
                    consider(evaluate(tu, lx))

# Random with finish1 bonus
random.seed(55)
print("Random finish1-biased...")
for _ in range(4000):
    team = []
    slots = 0
    counts = defaultdict(int)
    names = list(POOL)
    while slots < MAX_SLOTS:
        pick, bg = None, -99
        for n in names:
            if n in team:
                continue
            if n in ("Kha'Zix", "Rengar") and any(x in ("Kha'Zix", "Rengar") for x in team):
                continue
            if slots + U[n][2] > MAX_SLOTS:
                continue
            tr = defaultdict(int, counts)
            for t in nu(n):
                tr[t] += 1
            if n == "Elder Dragon":
                tr["Riftbeast"] += 2
            g = random.random() * 0.25
            for t, bp in BP.items():
                if counts[t] < bp <= tr[t]:
                    g += 6
                elif tr[t] == bp - 1 > counts[t]:
                    g += 3.5
                elif counts[t] < bp and tr[t] > counts[t]:
                    g += 0.35
            g += 0.3 * len(nu(n))
            if g > bg:
                bg, pick = g, n
        if pick is None:
            break
        team.append(pick)
        slots += U[pick][2]
        for t in nu(pick):
            counts[t] += 1
        if pick == "Elder Dragon":
            counts["Riftbeast"] += 2
    for lux in [None] + list(LUX.keys()):
        consider(evaluate(team, lux))

print("\n" + "=" * 60)
print("MAX:", best["n"] if best else None)
if best:
    print("units", best["units"])
    print("lux", best["lux"])
    print("em", best["em1"], best["em2"])
    print("base", best["base_n"], best["base"])
    print("add", best["add"])
    print("ACT", best["n"], best["act"])
    print("finish1", best["finish1"])
    for t in sorted(BP.keys()):
        c = best["counts"][t]
        print(f"  {t:16} {c}/{BP[t]} {'ACT' if t in best['act'] else ''}")
