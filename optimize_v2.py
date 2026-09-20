# -*- coding: utf-8 -*-
"""TFT Set 18 Enchanted Wilds (18.2b)
Max non-unique traits: <=11 slots + Fae emblem + Coven emblem
Lux Avatar form trait counts as 2.
"""
from collections import defaultdict
import itertools
import random

UNIQUE = {
    "Attuned", "Avatar", "Bounty Seeker", "Emerald Aspect", "Monolith",
    "Old Growth", "Thornmaiden", "Caustic", "Greenfather", "Apex Predator",
}

# Chinese display names (approximate official/localized)
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

# First activation breakpoint
BP = {
    "Adaptor": 2, "Brawler": 2, "Defender": 2, "Executioner": 2,
    "Hunter": 2, "Invoker": 2, "Juggernaut": 2, "Rapidfire": 2,
    "Ravager": 2, "Spellweaver": 2, "Summoner": 2, "Vanguard": 2,
    "Blossom": 3, "Coven": 3, "Elderwood": 3, "Blackthorn": 2,
    "Fae": 2, "Flora Fatalis": 1, "Inferno": 2, "Lunar": 2,
    "Primal": 2, "Riftbeast": 3, "Solar": 3, "Sprykin": 3,
    "Rival": 1,
}

# name -> (cost, traits, slots)
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
    "Elder Dragon": (5, ["Riftbeast", "Apex Predator"], 2),  # +2 Riftbeast
    "Gnar": (5, ["Elderwood", "Sprykin", "Brawler"], 1),
    "Ivern": (5, ["Greenfather"], 1),
    "Kennen": (5, ["Inferno", "Executioner"], 1),
    "Maokai": (5, ["Old Growth", "Juggernaut"], 1),
    "Taric": (5, ["Emerald Aspect", "Vanguard"], 1),
}

# Lux Avatar forms: form trait counts TWICE
LUX = {
    "Lux Fae": "Fae",
    "Lux Coven": "Coven",
    "Lux Solar": "Solar",
    "Lux Primal": "Primal",
    "Lux Blackthorn": "Blackthorn",
    "Lux Blossom": "Blossom",
    "Lux Inferno": "Inferno",
    "Lux Elderwood": "Elderwood",
    "Lux Lunar": "Lunar",
}

MAX_SLOTS = 11
FAE_NATIVE = {"Rakan", "Xayah", "Tristana", "Lillia"}
COVEN_NATIVE = {"Camille", "Caitlyn", "Elise", "Cassiopeia", "Morgana"}


def nu(name):
    return [t for t in U[name][1] if t not in UNIQUE]


def base_counts(team):
    c = defaultdict(int)
    for n in team:
        for t in U[n][1]:
            if t not in UNIQUE:
                c[t] += 1
        if n == "Elder Dragon":
            c["Riftbeast"] += 2
    return c


def add_lux(counts, lux_name):
    c = defaultdict(int, counts)
    c[LUX[lux_name]] += 2  # Avatar: chosen trait counts twice
    return c


def assign_emblems(counts, team, lux_name):
    """Fae emblem + Coven emblem on two different units that lack that trait.
    Returns best (activated_count, fae_on, coven_on, final_counts, activated_list)
    """
    # Units that can receive Fae emblem (don't already have Fae natively)
    fae_ok = []
    coven_ok = []
    for n in team:
        if n in LUX:
            # Lux form: has form trait, not Fae/Coven unless form is that
            form = LUX[n]
            if form != "Fae":
                fae_ok.append(n)
            if form != "Coven":
                coven_ok.append(n)
        else:
            if "Fae" not in U[n][1]:
                fae_ok.append(n)
            if "Coven" not in U[n][1]:
                coven_ok.append(n)

    best = (-1, None, None, None, None)
    # Emblems must go to different units (each unit one emblem item)
    for f in fae_ok:
        for cv in coven_ok:
            if f == cv:
                continue
            c = defaultdict(int, counts)
            c["Fae"] += 1
            c["Coven"] += 1
            act = [t for t, bp in BP.items() if c[t] >= bp]
            if len(act) > best[0]:
                best = (len(act), f, cv, c, act)
    # Degenerate: empty candidates for one emblem
    if best[0] < 0:
        c = defaultdict(int, counts)
        if fae_ok:
            c["Fae"] += 1
        if coven_ok:
            c["Coven"] += 1
        act = [t for t, bp in BP.items() if c[t] >= bp]
        best = (len(act), fae_ok[0] if fae_ok else None,
                coven_ok[0] if coven_ok else None, c, act)
    return best


def evaluate(team, lux_name):
    """Full evaluation of a composition."""
    units = list(team)
    slots = sum(U[n][2] for n in units)
    if lux_name:
        slots += 1  # lux occupies 1 slot
    if slots > MAX_SLOTS:
        return None
    # Rival: at most 1
    if sum(1 for n in units if n in ("Kha'Zix", "Rengar")) > 1:
        return None
    counts = base_counts(units)
    if lux_name:
        counts = add_lux(counts, lux_name)
        units_with_lux = units + [lux_name]
    else:
        units_with_lux = units
    n_act, fae_on, coven_on, final_c, act = assign_emblems(counts, units_with_lux, lux_name)
    return {
        "n": n_act,
        "units": units,
        "lux": lux_name,
        "slots": slots,
        "emblem_fae": fae_on,
        "emblem_coven": coven_on,
        "counts": final_c,
        "activated": act,
    }


POOL = [n for n in U if nu(n) or n == "Elder Dragon"]
# Elder Dragon contributes Riftbeast (non-unique) via +2
POOL = [n for n in U if any(t not in UNIQUE for t in U[n][1]) or n == "Elder Dragon"]
# Drop units whose only non-unique contribution is nothing
POOL = [n for n in U if nu(n) or n == "Elder Dragon"]
POOL.sort(key=lambda n: (-len(nu(n) + (["Riftbeast"] if n == "Elder Dragon" else [])), U[n][0], n))
print("Pool:", len(POOL))
print("Unique-only units excluded:", [n for n in U if n not in POOL])

# ---- Beam search over unit subsets + lux option ----
BEAM = 8000
best = None

def consider(res):
    global best
    if res is None:
        return
    if best is None or res["n"] > best["n"]:
        best = res
        print(f"NEW BEST {res['n']}: {res['units']} lux={res['lux']} "
              f"fae_em={res['emblem_fae']} coven_em={res['emblem_coven']}")
        print(f"  activated={sorted(res['activated'])}")


def partial_score(team):
    """Activated so far + optimistic remaining."""
    c = base_counts(team)
    act = sum(1 for t, bp in BP.items() if c[t] >= bp)
    # optimistic: remaining slots could still fire unactivated traits
    return act


# Expand beam
states = [tuple()]  # tuple of unit names
for step in range(len(POOL)):
    # evaluate all current + lux variants
    for st in states:
        for lux in [None] + list(LUX.keys()):
            consider(evaluate(list(st), lux))
    # expand
    nxt = []
    seen = set()
    for st in states:
        slots = sum(U[n][2] for n in st)
        if slots >= MAX_SLOTS:
            continue
        st_set = set(st)
        for name in POOL:
            if name in st_set:
                continue
            if name in ("Kha'Zix", "Rengar") and any(x in ("Kha'Zix", "Rengar") for x in st_set):
                continue
            if slots + U[name][2] > MAX_SLOTS:
                continue
            new = tuple(sorted(st + (name,), key=lambda x: (U[x][0], x)))
            if new not in seen:
                seen.add(new)
                nxt.append(new)
    # rank partials
    nxt.sort(key=lambda st: -partial_score(list(st)))
    states = nxt[:BEAM]
    if step % 5 == 0 or step < 5:
        print(f"  step {step}: beam={len(states)} best={best['n'] if best else None}")

print("\nBeam done. Best:", best["n"] if best else None)

# ---- Local search polish ----
def local_search(cur):
    improved = True
    rounds = 0
    while improved and rounds < 40:
        improved = False
        rounds += 1
        units = list(cur["units"])
        lux = cur["lux"]
        cur_n = cur["n"]
        pool_opts = list(POOL) + list(LUX.keys())
        # swaps
        for rm in units + ([lux] if lux else []):
            for add in pool_opts:
                if add == rm:
                    continue
                trial_units = [x for x in units if x != rm]
                trial_lux = lux
                if add in LUX:
                    if lux and lux != rm:
                        continue  # already have lux
                    trial_lux = add
                else:
                    if add in trial_units:
                        continue
                    trial_units = trial_units + [add]
                    if rm == lux:
                        trial_lux = None
                res = evaluate(trial_units, trial_lux)
                if res and res["n"] > cur_n:
                    cur = res
                    improved = True
                    print(f"  swap {rm}->{add}: {res['n']}")
                    break
            if improved:
                break
        # adds
        if not improved:
            slots = cur["slots"]
            if slots < MAX_SLOTS:
                for add in pool_opts:
                    if add in units or add == lux:
                        continue
                    if add in LUX and lux:
                        continue
                    sc = 1 if add in LUX else U[add][2]
                    if slots + sc > MAX_SLOTS:
                        continue
                    if add in LUX:
                        res = evaluate(units, add)
                    else:
                        res = evaluate(units + [add], lux)
                    if res and res["n"] > cur_n:
                        cur = res
                        improved = True
                        print(f"  add {add}: {res['n']}")
                        break
        # removes
        if not improved:
            for rm in units + ([lux] if lux else []):
                if rm in LUX:
                    res = evaluate(units, None)
                else:
                    res = evaluate([x for x in units if x != rm], lux)
                if res and res["n"] > cur_n:
                    cur = res
                    improved = True
                    print(f"  remove {rm}: {res['n']}")
                    break
    return cur

if best:
    best = local_search(best)

# ---- Targeted exhaustive around high-value patterns ----
# Try all combinations of size 8-11 from a reduced elite pool + lux
elite = POOL[:28]
print("\nElite pool size:", len(elite))
for size in range(8, 12):
    # too many C(28,11); sample structured combos instead
    pass

# Structured: pick units that complete many 2-traits
# Greedy constructive + random restarts
random.seed(1)
for restart in range(200):
    team = []
    lux = None
    slots = 0
    counts = defaultdict(int)
    # randomly build prioritizing new/underfilled non-unique traits
    candidates = list(POOL)
    random.shuffle(candidates)
    # force include some high-connector units sometimes
    if restart % 3 == 0:
        seeds = random.sample(POOL, min(4, len(POOL)))
        for s in seeds:
            if U[s][2] + slots <= MAX_SLOTS:
                team.append(s)
                slots += U[s][2]
                for t in nu(s):
                    counts[t] += 1
                if s == "Elder Dragon":
                    counts["Riftbeast"] += 2
    while slots < MAX_SLOTS:
        best_pick = None
        best_gain = -1
        for name in candidates:
            if name in team:
                continue
            if name in ("Kha'Zix", "Rengar") and any(x in ("Kha'Zix", "Rengar") for x in team):
                continue
            if slots + U[name][2] > MAX_SLOTS:
                continue
            # gain = newly activated or closer to BP
            gain = 0
            trial = defaultdict(int, counts)
            for t in nu(name):
                trial[t] += 1
            if name == "Elder Dragon":
                trial["Riftbeast"] += 2
            for t, bp in BP.items():
                if counts[t] < bp and trial[t] >= bp:
                    gain += 3
                elif counts[t] < bp and trial[t] > counts[t]:
                    gain += 1
            # small bonus for multi-trait units
            gain += 0.1 * len(nu(name))
            if gain > best_gain:
                best_gain = gain
                best_pick = name
        if best_pick is None:
            break
        team.append(best_pick)
        slots += U[best_pick][2]
        for t in nu(best_pick):
            counts[t] += 1
        if best_pick == "Elder Dragon":
            counts["Riftbeast"] += 2
    # try all lux
    for lux_name in [None] + list(LUX.keys()):
        res = evaluate(team, lux_name)
        consider(res)

if best:
    best = local_search(best)

# ---- Manual high-synergy constructions ----
manual_teams = [
    # Broad 2-trait mesh
    ["Rakan", "Xayah", "Tristana", "Lillia", "Caitlyn", "Elise", "Camille",
     "Yunara", "Fiddlesticks", "Morgana", "Soraka"],
    ["Rakan", "Xayah", "Karma", "Yorick", "Yunara", "Ahri", "Master Yi",
     "Ashe", "Sett", "Kobuko", "Gnar"],
    ["Akali", "Varus", "Shen", "Kennen", "Amumu", "Camille", "Murkwolf",
     "Warwick", "Diana", "Brambleback", "Cinderling"],
    ["Rakan", "Xayah", "Tristana", "Lillia", "Veigar", "Cassiopeia",
     "Caitlyn", "Morgana", "Elise", "Fiddlesticks", "Soraka"],
    ["Xayah", "Rakan", "Kayle", "Leona", "Sejuani", "Ornn", "Alistar",
     "Ezreal", "Gnar", "Hecarim", "LeBlanc"],
    ["Rakan", "Tristana", "Lillia", "Xayah", "Vi", "Nidalee", "Sivir",
     "Kog'Maw", "Gromp", "Master Yi", "Teemo"],
    ["Caitlyn", "Camille", "Elise", "Cassiopeia", "Morgana", "Rakan",
     "Xayah", "Yunara", "Fiddlesticks", "Soraka", "Tristana"],
    ["Rakan", "Xayah", "Tristana", "Lillia", "Caitlyn", "Camille",
     "Yorick", "Karma", "Yunara", "Ahri", "Zyra"],
    ["Akali", "Camille", "Cinderling", "Karma", "Rakan", "Rek'Sai",
     "Varus", "Veigar", "Xayah", "Yorick", "Caitlyn"],
    ["Rakan", "Xayah", "Diana", "Aphelios", "Alune", "Kayle", "Leona",
     "Sejuani", "Fiddlesticks", "Soraka", "Tristana"],
]
for team in manual_teams:
    # validate slots
    if sum(U[n][2] for n in team) > MAX_SLOTS:
        continue
    for lux_name in [None] + list(LUX.keys()):
        res = evaluate(team, lux_name)
        consider(res)

if best:
    best = local_search(best)

# ---- Exhaustive on small core sets (pairs/triples covering traits) ----
# For each non-unique trait pick 2-3 members, union them if size/slots allow
trait_members = defaultdict(list)
for n, (cost, traits, sc) in U.items():
    for t in traits:
        if t not in UNIQUE:
            trait_members[t].append(n)
    if n == "Elder Dragon":
        trait_members["Riftbeast"].append(n)

print("\nTrait member counts:")
for t in sorted(BP.keys(), key=lambda x: BP[x]):
    print(f"  {t} (BP {BP[t]}): {len(trait_members[t])} {trait_members[t]}")

# Try combinations choosing 2 members for BP=2 traits, 3 for BP=3, 1 for BP=1
# This is large; instead pick random subsets of 2 per trait and union
random.seed(2)
for _ in range(5000):
    team_set = []
    slots = 0
    for t, bp in BP.items():
        members = trait_members[t]
        if len(members) < bp:
            continue
        need = bp
        # Lux can supply 2 of Fae/Coven/form
        picked = random.sample(members, min(need, len(members)))
        for p in picked:
            if p in LUX:
                continue  # lux handled separately
            if p in team_set:
                continue
            if p in ("Kha'Zix", "Rengar") and any(x in ("Kha'Zix", "Rengar") for x in team_set):
                continue
            if slots + U[p][2] > MAX_SLOTS:
                continue
            team_set.append(p)
            slots += U[p][2]
    for lux_name in [None] + list(LUX.keys()):
        res = evaluate(team_set, lux_name)
        consider(res)

if best:
    best = local_search(best)

print("\n" + "=" * 60)
print("FINAL MAX NON-UNIQUE TRAITS:", best["n"] if best else None)
if best:
    print("Units:", best["units"])
    print("Lux:", best["lux"], f"(counts as 2 x {LUX[best['lux']]})" if best["lux"] else "")
    print("Fae emblem on:", best["emblem_fae"])
    print("Coven emblem on:", best["emblem_coven"])
    print("Slots:", best["slots"])
    print("Activated traits:")
    for t in sorted(best["activated"], key=lambda x: (-best["counts"][x], x)):
        print(f"  {t} ({CN.get(t,t)}): {best['counts'][t]}/{BP[t]}")
    print("\nAll non-unique trait counts:")
    for t in sorted(BP.keys()):
        c = best["counts"][t]
        mark = "ACTIVATED" if c >= BP[t] else "-"
        print(f"  {t:16} {CN.get(t,'?'):8}  {c}/{BP[t]}  {mark}")
    print("\nUnit details:")
    for n in best["units"]:
        print(f"  {n} ({U[n][0]}*, slots {U[n][2]}): {U[n][1]}")
    if best["lux"]:
        print(f"  {best['lux']} (5*, slots 1): Avatar + {LUX[best['lux']]} (counts x2)")
