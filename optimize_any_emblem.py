# -*- coding: utf-8 -*-
"""Fixed: 2 free emblems maximize UNIQUE activated non-unique traits."""
from collections import defaultdict
import random
import itertools

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
    # traits where 1 emblem finishes them
    finish1 = []  # (trait, eligible_units)
    # traits where 2 emblems of same trait finish them
    finish2 = []  # (trait, eligible_units >=2)
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

    # Max unique additions with 2 emblems:
    # Option A: two different finish1 traits on two different units (+2)
    # Option B: one finish1 + cannot use second productively unless another finish1
    # Option C: one finish2 (+1)
    best_add = set()
    best_em = (None, None)
    # try pairs of finish1
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
    if len(best_add) < 2:
        # single finish1
        if finish1 and len(best_add) < 1:
            t, e = finish1[0]
            best_add = {t}
            best_em = ((e[0], t), None)
        elif finish1 and len(best_add) == 1:
            # try add second finish1 different trait
            have_t = next(iter(best_add))
            for t, e in finish1:
                if t == have_t:
                    continue
                u_have = best_em[0][0]
                for u in e:
                    if u != u_have:
                        best_add = {have_t, t}
                        best_em = (best_em[0], (u, t))
                        break
                if len(best_add) == 2:
                    break
    if len(best_add) < 1 and finish2:
        t, e = finish2[0]
        best_add = {t}
        best_em = ((e[0], t), (e[1], t))
    elif len(best_add) == 1 and finish2:
        # can second emblem help finish2? need 2 emblems - no
        pass
    elif len(best_add) == 0 and finish2:
        t, e = finish2[0]
        best_add = {t}
        best_em = ((e[0], t), (e[1], t))

    act = already | best_add
    final_c = defaultdict(int, counts)
    if best_em[0]:
        final_c[best_em[0][1]] += 1
    if best_em[1]:
        final_c[best_em[1][1]] += 1

    return dict(
        n=len(act), units=list(units), lux=lux, slots=slots,
        em1=best_em[0], em2=best_em[1], act=sorted(act), counts=dict(final_c),
        base=sorted(already), add=sorted(best_add),
        finish1=[t for t, _ in finish1], finish2=[t for t, _ in finish2],
        base_n=len(already),
    )

POOL = [n for n in U if nu(n) or n == "Elder Dragon"]
best = None

def consider(r):
    global best
    if not r:
        return
    if best is None or r["n"] > best["n"] or (
        r["n"] == best["n"] and r["base_n"] > best.get("base_n", 0)
    ):
        if best is None or r["n"] > best["n"]:
            print(f"NEW BEST {r['n']} (base {r['base_n']}+{r['add']}): {r['units']} lux={r['lux']}")
            print(f"  emblems: {r['em1']} | {r['em2']}")
            print(f"  finish1={r['finish1']} finish2={r['finish2']}")
            print(f"  ACT: {r['act']}")
        best = r if (best is None or r["n"] >= best["n"]) else best
        if r["n"] >= (best["n"] if best else 0):
            best = r

def local(cur):
    if not cur:
        return cur
    improved = True
    rounds = 0
    while improved and rounds < 35:
        improved = False
        rounds += 1
        units, lux, cur_n = list(cur["units"]), cur["lux"], cur["n"]
        opts = list(POOL) + list(LUX.keys())
        for rm in units + ([lux] if lux else []):
            for add in opts:
                if add == rm or add in units or add == lux:
                    continue
                tu, tl = list(units), lux
                if rm in LUX:
                    tl = None
                else:
                    tu = [x for x in units if x != rm]
                if add in LUX:
                    if tl:
                        continue
                    tl = add
                else:
                    tu = tu + [add]
                r = evaluate(tu, tl)
                if r and r["n"] > cur_n:
                    cur, improved = r, True
                    print(f"  swap {rm}->{add}: {r['n']} base={r['base_n']}+{r['add']}")
                    break
            if improved:
                break
        if not improved:
            for add in opts:
                if add in units or add == lux:
                    continue
                if add in LUX and lux:
                    continue
                sc = 1 if add in LUX else U[add][2]
                if cur["slots"] + sc > MAX_SLOTS:
                    continue
                r = evaluate(units + ([] if add in LUX else [add]), add if add in LUX else lux)
                if r and r["n"] > cur_n:
                    cur, improved = r, True
                    print(f"  add {add}: {r['n']}")
                    break
        if not improved:
            for rm in units + ([lux] if lux else []):
                r = evaluate(units, None) if rm in LUX else evaluate([x for x in units if x != rm], lux)
                if r and r["n"] > cur_n:
                    cur, improved = r, True
                    print(f"  remove {rm}: {r['n']}")
                    break
    return cur

seeds = [
    ["Rakan", "Yorick", "Shen", "Warwick", "Azir", "Diana", "Fiddlesticks", "Kha'Zix", "Alune", "Kennen"],
    ["Akali", "Rakan", "Shen", "Diana", "Fiddlesticks", "Vi", "Nidalee", "Alune", "Kennen", "Yorick"],
    ["Akali", "Varus", "Shen", "Kennen", "Amumu", "Camille", "Murkwolf", "Warwick", "Diana", "Fiddlesticks", "Rakan"],
    ["Rakan", "Yorick", "Karma", "Yunara", "Ahri", "Sett", "Kobuko", "Tristana", "Caitlyn", "Fiddlesticks", "Soraka"],
    ["Xayah", "Rakan", "Kayle", "Leona", "Sejuani", "Ornn", "Alistar", "Ezreal", "Gnar", "Hecarim", "LeBlanc"],
    ["Rakan", "Tristana", "Lillia", "Xayah", "Vi", "Nidalee", "Sivir", "Kog'Maw", "Gromp", "Master Yi", "Teemo"],
    ["Caitlyn", "Camille", "Elise", "Cassiopeia", "Morgana", "Rakan", "Yunara", "Fiddlesticks", "Soraka", "Yorick", "Karma"],
    ["Akali", "Gromp", "Kog'Maw", "Master Yi", "Nidalee", "Rakan", "Vi", "Veigar", "Warwick", "Fiddlesticks", "Kennen"],
    ["Rakan", "Yorick", "Azir", "Mama Beak", "Zyra", "Caitlyn", "Sivir", "Ashe", "Fiddlesticks", "Soraka", "Kennen"],
    ["Pebbles", "Teemo", "Kog'Maw", "Sentinel", "Morgana", "Rakan", "Diana", "Hecarim", "Fiddlesticks", "Akali", "Yorick"],
    ["Kobuko", "Rek'Sai", "Alistar", "Krug", "Sett", "Gnar", "Rakan", "Yorick", "Tristana", "Fiddlesticks", "Camille"],
    ["Leona", "Ornn", "Shen", "Fiddlesticks", "Rammus", "Lillia", "Rakan", "Diana", "Warwick", "Azir", "Yorick"],
    ["Cinderling", "Caitlyn", "Tristana", "Sivir", "Ashe", "Rakan", "Yorick", "Fiddlesticks", "Soraka", "Camille", "Karma"],
    ["Varus", "Xayah", "Kayle", "Mama Beak", "Aphelios", "Rakan", "Diana", "Fiddlesticks", "Alune", "Kennen", "Yorick"],
    ["Akali", "Camille", "Murkwolf", "Warwick", "Diana", "Brambleback", "Rakan", "Shen", "Fiddlesticks", "Azir", "Yorick"],
    ["Karma", "Veigar", "LeBlanc", "Cassiopeia", "Fiddlesticks", "Ahri", "Alune", "Rakan", "Yorick", "Diana", "Kennen"],
    ["Pebbles", "Fiddlesticks", "Sentinel", "Mama Beak", "Azir", "Veigar", "Diana", "Aphelios", "Akali", "Kennen", "Lillia"],
    ["Rakan", "Xayah", "Tristana", "Lillia", "Caitlyn", "Elise", "Yunara", "Soraka", "Yorick", "Fiddlesticks", "Karma"],
    ["Yorick", "Azir", "Mama Beak", "Zyra", "Karma", "Ahri", "Yunara", "Ashe", "Sett", "Master Yi", "Fiddlesticks"],
    ["Ornn", "Xayah", "Alistar", "LeBlanc", "Hecarim", "Ezreal", "Gnar", "Leona", "Kayle", "Sejuani", "Rakan"],
    ["Kobuko", "Veigar", "Teemo", "Rammus", "Tristana", "Gnar", "Rek'Sai", "Alistar", "Sett", "Krug", "Fiddlesticks"],
    ["Cinderling", "Gromp", "Pebbles", "Murkwolf", "Scuttlecrab", "Krug", "Mama Beak", "Sentinel", "Brambleback", "Akali", "Kennen"],
    ["Caitlyn", "Cinderling", "Tristana", "Sivir", "Ashe", "Akali", "Camille", "Yorick", "Azir", "Fiddlesticks", "Soraka"],
    ["Rakan", "Yorick", "Shen", "Warwick", "Azir", "Diana", "Fiddlesticks", "Kennen", "Alune", "Morgana", "Caitlyn"],
    ["Akali", "Rakan", "Yorick", "Shen", "Diana", "Fiddlesticks", "Vi", "Nidalee", "Kennen", "Karma", "Veigar"],
    ["Akali", "Camille", "Rakan", "Yorick", "Shen", "Warwick", "Azir", "Diana", "Fiddlesticks", "Kennen", "Tristana"],
    ["Kog'Maw", "Gromp", "Master Yi", "Nidalee", "Akali", "Rakan", "Vi", "Teemo", "Pebbles", "Sentinel", "Fiddlesticks"],
    ["Leona", "Kayle", "Sejuani", "Ornn", "Xayah", "Alistar", "Ezreal", "Rakan", "Diana", "Fiddlesticks", "Yorick"],
    ["Camille", "Caitlyn", "Elise", "Cassiopeia", "Morgana", "Yunara", "Soraka", "Fiddlesticks", "Karma", "Ahri", "Rakan"],
    ["Varus", "Xayah", "Kayle", "Aphelios", "Mama Beak", "Akali", "Shen", "Kennen", "Amumu", "Rakan", "Diana"],
    # designed: many BP2 pairs + leftover singles
    ["Akali", "Gromp", "Rakan", "Yorick", "Shen", "Warwick", "Azir", "Diana", "Fiddlesticks", "Kennen", "Vi"],
    ["Akali", "Master Yi", "Nidalee", "Kog'Maw", "Gromp", "Rakan", "Yorick", "Fiddlesticks", "Kennen", "Diana", "Vi"],
    ["Camille", "Warwick", "Murkwolf", "Akali", "Diana", "Brambleback", "Rakan", "Yorick", "Shen", "Fiddlesticks", "Kennen"],
    ["Caitlyn", "Cinderling", "Tristana", "Ashe", "Sivir", "Rakan", "Yorick", "Fiddlesticks", "Soraka", "Karma", "Yunara"],
    ["Pebbles", "Teemo", "Sentinel", "Morgana", "Kog'Maw", "Rakan", "Yorick", "Fiddlesticks", "Akali", "Diana", "Kennen"],
    ["Veigar", "Warwick", "Rek'Sai", "Azir", "Malphite", "Rakan", "Yorick", "Fiddlesticks", "Karma", "Alune", "Diana"],
    ["Leona", "Kayle", "Sejuani", "Ornn", "Alistar", "Ezreal", "Gnar", "LeBlanc", "Hecarim", "Xayah", "Rakan"],
    ["Kobuko", "Rammus", "Teemo", "Veigar", "Tristana", "Gnar", "Sett", "Krug", "Alistar", "Fiddlesticks", "Rakan"],
    ["Yorick", "Karma", "Yunara", "Ahri", "Ashe", "Sett", "Master Yi", "Azir", "Mama Beak", "Zyra", "Fiddlesticks"],
    ["Cinderling", "Gromp", "Murkwolf", "Scuttlecrab", "Krug", "Mama Beak", "Pebbles", "Sentinel", "Brambleback", "Akali", "Kennen"],
]

print("Seeds + lux...")
for team in seeds:
    if sum(U[n][2] for n in team) > MAX_SLOTS:
        continue
    for lux in [None] + list(LUX.keys()):
        consider(evaluate(team, lux))
if best:
    best = local(best)

random.seed(33)
print("Constructive: maximize base + 2 finish1...")
for restart in range(3000):
    team = []
    slots = 0
    counts = defaultdict(int)
    names = list(POOL)
    while slots < MAX_SLOTS:
        # score by: complete traits + create finish1 opportunities
        pick, bestg = None, -99
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
            g = random.random() * 0.2
            for t, bp in BP.items():
                if counts[t] < bp <= tr[t]:
                    g += 5
                elif tr[t] == bp - 1 and counts[t] < bp - 1:
                    # lands on need=1 (emblem gold)
                    g += 3
                elif counts[t] < bp and tr[t] > counts[t]:
                    g += 0.4
            g += 0.25 * len(nu(n))
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
        consider(evaluate(team, lux))
if best:
    best = local(best)

print("Neighborhood from best...")
if best:
    units0 = list(best["units"])
    lux0 = best["lux"]
    for i in range(len(units0)):
        for a in POOL:
            if a in units0:
                continue
            tu = list(units0)
            tu[i] = a
            r = evaluate(tu, lux0)
            if r:
                consider(r)
        # replace with lux
        if not lux0:
            for lx in LUX:
                tu = list(units0)
                # drop unit i, add lux
                tu.pop(i) if False else None
                tu2 = [units0[j] for j in range(len(units0)) if j != i]
                r = evaluate(tu2, lx)
                if r:
                    consider(r)
    best = local(best)

# Elite random
print("Elite combos...")
elite = sorted(POOL, key=lambda n: -len(nu(n)))[:26]
random.seed(77)
for _ in range(5000):
    team = []
    slots = 0
    # pick 10-11 units from elite with connector bias
    pool_e = list(elite)
    random.shuffle(pool_e)
    for n in pool_e:
        if n in team:
            continue
        if n in ("Kha'Zix", "Rengar") and any(x in ("Kha'Zix", "Rengar") for x in team):
            continue
        if slots + U[n][2] > MAX_SLOTS:
            continue
        if random.random() < 0.7 or len(team) < 6:
            team.append(n)
            slots += U[n][2]
        if slots >= MAX_SLOTS:
            break
    for lux in [None] + list(LUX.keys()):
        consider(evaluate(team, lux))
if best:
    best = local(best)

print("\n" + "=" * 60)
print("FINAL MAX UNIQUE NON-UNIQUE TRAITS:", best["n"] if best else None)
if best:
    print("Units:", best["units"])
    print("Lux:", best["lux"], f"({LUX[best['lux']] } x2)" if best["lux"] else "(none)")
    print("Slots:", best["slots"])
    print("Emblem1:", best["em1"])
    print("Emblem2:", best["em2"])
    print("Base activated:", best["base_n"], best["base"])
    print("Emblem adds:", best["add"])
    print("Total ACT:", best["n"], best["act"])
    print("\nBoard:")
    for n in best["units"]:
        print(f"  {n} ({U[n][0]}*): {U[n][1]}")
    if best["lux"]:
        print(f"  {best['lux']}: Avatar + {LUX[best['lux']]} x2")
    print("\nCounts:")
    for t in sorted(BP.keys()):
        c = best["counts"][t]
        print(f"  {t:16} {CN.get(t,'?'):8} {c}/{BP[t]} {'ACT' if t in best['act'] else ''}")
