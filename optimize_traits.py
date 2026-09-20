"""Beam + local search for max non-unique traits in TFT Set 18."""
from collections import defaultdict
import random

UNIQUE_TRAITS = {
    "Attuned", "Avatar", "Bounty Seeker", "Emerald Aspect", "Monolith",
    "Old Growth", "Thornmaiden", "Caustic", "Greenfather", "Apex Predator",
}

BREAKPOINTS = {
    "Adaptor": 2, "Brawler": 2, "Defender": 2, "Executioner": 2,
    "Hunter": 2, "Invoker": 2, "Juggernaut": 2, "Rapidfire": 2,
    "Ravager": 2, "Spellweaver": 2, "Summoner": 2, "Vanguard": 2,
    "Blossom": 3, "Coven": 3, "Elderwood": 3, "Blackthorn": 2,
    "Fae": 2, "Flora Fatalis": 1, "Inferno": 2, "Lunar": 2,
    "Primal": 2, "Riftbeast": 3, "Solar": 3, "Sprykin": 3,
    "Rival": 1,
}

UNITS = {
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

LUX_FORMS = {
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

MAX_SLOTS = 10
FAE_NATIVE = {"Rakan", "Xayah", "Tristana", "Lillia"}


def nu_traits(name):
    return [t for t in UNITS[name][1] if t not in UNIQUE_TRAITS]


def make_state():
    return {"team": [], "slots": 0, "counts": defaultdict(int), "has_lux": False}


def add_unit(state, name):
    cost, traits, sc = UNITS[name]
    state["team"].append(name)
    state["slots"] += sc
    for t in traits:
        if t not in UNIQUE_TRAITS:
            state["counts"][t] += 1
    if name == "Elder Dragon":
        state["counts"]["Riftbeast"] += 2  # extra +2 from Apex Predator


def clone(state):
    return {
        "team": list(state["team"]),
        "slots": state["slots"],
        "counts": defaultdict(int, state["counts"]),
        "has_lux": state["has_lux"],
    }


def apply_lux(state, lux_name):
    st = clone(state)
    if st["slots"] + 1 > MAX_SLOTS:
        return None
    origin = LUX_FORMS[lux_name]
    st["counts"][origin] += 1
    st["slots"] += 1
    st["team"].append(lux_name)
    st["has_lux"] = True
    return st


def activated(counts):
    return [t for t, bp in BREAKPOINTS.items() if counts.get(t, 0) >= bp]


def score_with_emblem(state):
    """Return (best_count, emblem_target, activated_list, counts_final)."""
    counts = defaultdict(int, state["counts"])
    # Emblem can go to any team member that doesn't natively have Fae
    native_fae = 0
    for name in state["team"]:
        if name in FAE_NATIVE or name == "Lux Fae":
            native_fae += 1
        # Lux form Fae already counted in counts via apply_lux
    # Fae count without emblem is counts['Fae']
    base_fae = counts.get("Fae", 0)
    # Candidates: units on board without Fae
    candidates = []
    for name in state["team"]:
        if name in FAE_NATIVE or name == "Lux Fae":
            continue
        if name in LUX_FORMS and LUX_FORMS[name] == "Fae":
            continue
        candidates.append(name)

    best_n = -1
    best_em = None
    best_act = None
    best_c = None
    if not candidates:
        act = activated(counts)
        return len(act), None, act, counts
    for target in candidates:
        c = defaultdict(int, counts)
        c["Fae"] += 1
        act = activated(c)
        if len(act) > best_n:
            best_n = len(act)
            best_em = target
            best_act = act
            best_c = c
    return best_n, best_em, best_act, best_c


def optimistic(state, pool_from):
    """Upper bound on final activated count if we fill remaining slots optimistically."""
    counts = defaultdict(int, state["counts"])
    slots_left = MAX_SLOTS - state["slots"]
    # remaining potential trait increments
    rem = defaultdict(int)
    selected = set(state["team"])
    for name in UNITS:
        if name in selected:
            continue
        sc = UNITS[name][2]
        # each unselected unit could still be added if slots allow — count all as potential
        for t in nu_traits(name):
            rem[t] += 1
        if name == "Elder Dragon":
            rem["Riftbeast"] += 2
    # emblem + lux
    rem["Fae"] += 1
    if not state["has_lux"]:
        for origin in LUX_FORMS.values():
            rem[origin] += 1
    # Very loose: ignore that rem units compete for slots; still useful prune only when even this is low
    # Tighten: at most slots_left more unit-slots of traits; cap rem by ~3*slots_left total
    total_rem = sum(rem.values())
    cap = 3 * slots_left + 3  # lux/emblem slack
    if total_rem > cap:
        # scale down proportionally — still optimistic if we only count first `cap` best
        pass
    n = 0
    for t, bp in BREAKPOINTS.items():
        have = counts.get(t, 0)
        if have >= bp:
            n += 1
        elif have + rem.get(t, 0) >= bp:
            # only count if slots_left can plausibly provide remaining
            need = bp - have
            if need <= slots_left + 2:  # lux/emblem
                n += 1
    return n


# Filter useful pool
POOL = [n for n in UNITS if nu_traits(n)]
POOL.sort(key=lambda n: (-len(nu_traits(n)), UNITS[n][0], n))
print("Pool size:", len(POOL))
print("Pool order sample:", POOL[:20])

# Beam search
BEAM = 20000

def beam_search():
    beam = [make_state()]
    best = (-1, None, None, None, None)  # n, team, lux, emblem, acts

    def consider(st):
        nonlocal best
        # try without lux if already has lux slot counted, and with lux if not
        variants = []
        if st["has_lux"]:
            variants.append(st)
        else:
            variants.append(st)
            if st["slots"] + 1 <= MAX_SLOTS:
                for lx in LUX_FORMS:
                    s2 = apply_lux(st, lx)
                    if s2:
                        variants.append(s2)
        for v in variants:
            n, em, acts, c = score_with_emblem(v)
            if n > best[0]:
                best = (n, list(v["team"]), v["has_lux"] and v["team"][-1] if v["has_lux"] else (
                    v["team"][-1] if v["team"] and v["team"][-1] in LUX_FORMS else None
                ), em, acts)
                # cleaner lux extraction
                lux = None
                for name in v["team"]:
                    if name in LUX_FORMS:
                        lux = name
                best = (n, list(v["team"]), lux, em, acts)
                print(f"NEW BEST {n}: {v['team']} lux={lux} emblem={em}")
                print(f"  acts={acts}")

    # Process in cost order roughly — expand by adding next units
    # Two-phase: first without lux in pool, lux applied at consider time
    for step in range(len(POOL)):
        new_beam = []
        # always keep evaluating current beam
        for st in beam:
            consider(st)
            if st["slots"] >= MAX_SLOTS:
                new_beam.append(st)
                continue
            # expand
            for name in POOL:
                if name in st["team"]:
                    continue
                sc = UNITS[name][2]
                if st["slots"] + sc > MAX_SLOTS:
                    continue
                if name in ("Kha'Zix", "Rengar") and any(x in ("Kha'Zix", "Rengar") for x in st["team"]):
                    continue
                # limit rival to 1
                nst = clone(st)
                add_unit(nst, name)
                new_beam.append(nst)
        # dedupe by frozenset team + slots
        seen = {}
        for st in new_beam:
            key = (frozenset(st["team"]), st["slots"], st["has_lux"])
            # score partial by activated + optimistic
            sc = len(activated(st["counts"])) + 0.3 * optimistic(st, 0)
            if key not in seen or sc > seen[key][0]:
                seen[key] = (sc, st)
        ranked = sorted(seen.values(), key=lambda x: -x[0])
        beam = [st for _, st in ranked[:BEAM]]
        print(f"step {step}: beam={len(beam)} best_so_far={best[0]}")

    # final consider all beam
    for st in beam:
        consider(st)

    print("\n===== FINAL =====")
    print("Max non-unique traits:", best[0])
    print("Team:", best[1])
    print("Lux:", best[2])
    print("Emblem on:", best[3])
    print("Activated:", sorted(best[4]) if best[4] else None)
    if best[1] and best[2]:
        team = [x for x in best[1] if x != best[2]]
        # rebuild counts display
        counts = defaultdict(int)
        for name in team:
            for t in UNITS[name][1]:
                if t not in UNIQUE_TRAITS:
                    counts[t] += 1
            if name == "Elder Dragon":
                counts["Riftbeast"] += 2
        if best[2]:
            counts[LUX_FORMS[best[2]]] += 1
        counts["Fae"] += 1  # emblem
        print("Trait counts:")
        for t in sorted(BREAKPOINTS, key=lambda x: -counts.get(x, 0)):
            print(f"  {t}: {counts.get(t,0)} (need {BREAKPOINTS[t]}) {'ACT' if counts.get(t,0)>=BREAKPOINTS[t] else ''}")
    return best


random.seed(42)
best = beam_search()

# Local search polish
print("\n===== LOCAL SEARCH =====")


def eval_team(team_names_with_lux):
    """team includes lux form name optionally."""
    lux = None
    units = []
    for n in team_names_with_lux:
        if n in LUX_FORMS:
            lux = n
        else:
            units.append(n)
    st = make_state()
    for n in units:
        if UNITS[n][2] + st["slots"] > MAX_SLOTS:
            return -1, None, None, None
        if n in ("Kha'Zix", "Rengar") and any(x in ("Kha'Zix", "Rengar") for x in st["team"]):
            return -1, None, None, None
        add_unit(st, n)
    if lux:
        st2 = apply_lux(st, lux)
        if not st2:
            return -1, None, None, None
        st = st2
    n, em, acts, c = score_with_emblem(st)
    return n, st["team"], em, acts


current = best[1] or []
current_n = best[0]
improved = True
round_i = 0
while improved and round_i < 30:
    improved = False
    round_i += 1
    # try swaps
    candidates_remove = [x for x in current if x not in LUX_FORMS]
    for rm in candidates_remove:
        for add in POOL + list(LUX_FORMS.keys()):
            if add in current:
                continue
            trial = [x for x in current if x != rm] + [add]
            n, team, em, acts = eval_team(trial)
            if n > current_n:
                current_n = n
                current = team
                best = (n, team, next((x for x in team if x in LUX_FORMS), None), em, acts)
                print(f"SWAP + : {n} {team} em={em}")
                improved = True
    # try add if slots left
    st_check = make_state()
    slots = 0
    for x in current:
        if x in LUX_FORMS:
            slots += 1
        else:
            slots += UNITS[x][2]
    if slots < MAX_SLOTS:
        for add in POOL + list(LUX_FORMS.keys()):
            if add in current:
                continue
            if add in LUX_FORMS and any(x in LUX_FORMS for x in current):
                continue
            sc = 1 if add in LUX_FORMS else UNITS[add][2]
            if slots + sc > MAX_SLOTS:
                continue
            trial = current + [add]
            n, team, em, acts = eval_team(trial)
            if n > current_n:
                current_n = n
                current = team
                best = (n, team, next((x for x in team if x in LUX_FORMS), None), em, acts)
                print(f"ADD + : {n} {team} em={em}")
                improved = True
    # try remove
    if current:
        for rm in list(current):
            trial = [x for x in current if x != rm]
            n, team, em, acts = eval_team(trial)
            if n > current_n:
                current_n = n
                current = team
                best = (n, team, next((x for x in team if x in LUX_FORMS), None), em, acts)
                print(f"RM + : {n} {team} em={em}")
                improved = True

print("\n===== OPTIMAL CANDIDATE =====")
print("Count:", best[0])
print("Team:", best[1])
print("Lux:", best[2])
print("Emblem:", best[3])
print("Activated:", sorted(best[4]) if best[4] else None)

# Detailed breakdown
if best[1]:
    team = list(best[1])
    lux = best[2]
    units = [x for x in team if x not in LUX_FORMS]
    counts = defaultdict(int)
    print("\nUnit traits:")
    for name in units:
        ts = UNITS[name][1]
        print(f"  {name} ({UNITS[name][0]}*): {ts}")
        for t in ts:
            if t not in UNIQUE_TRAITS:
                counts[t] += 1
        if name == "Elder Dragon":
            counts["Riftbeast"] += 2
            print(f"    -> Apex Predator: +2 Riftbeast, uses 2 slots")
    if lux:
        print(f"  {lux}: +1 {LUX_FORMS[lux]}")
        counts[LUX_FORMS[lux]] += 1
    print(f"  Fae Emblem on {best[3]}: +1 Fae")
    counts["Fae"] += 1
    print("\nBreakpoint check:")
    act_list = []
    for t, bp in BREAKPOINTS.items():
        c = counts.get(t, 0)
        mark = "YES" if c >= bp else "no"
        if c >= bp:
            act_list.append(t)
        print(f"  {t}: {c}/{bp} {mark}")
    print(f"\nActivated non-unique traits ({len(act_list)}): {act_list}")
    print(f"Slots used: {sum(UNITS[n][2] for n in units) + (1 if lux else 0)}")
