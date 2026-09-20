from pathlib import Path
import re

text = Path(
    r"C:\Users\jscjc\.local\share\mimocode\tool-output\tool_g001a0bf05ddbe001MxH9nEPpI"
).read_text(encoding="utf-8", errors="ignore")

KNOWN = {
    "Inferno", "Adaptor", "Ravager", "Coven", "Riftbeast", "Hunter", "Blossom",
    "Spellweaver", "Sprykin", "Brawler", "Solar", "Defender", "Elderwood", "Fae",
    "Juggernaut", "Vanguard", "Blackthorn", "Rapidfire", "Invoker", "Executioner",
    "Flora Fatalis", "Lunar", "Primal", "Rival", "Caustic", "Summoner",
    "Bounty Seeker", "Attuned", "Avatar", "Emerald Aspect", "Monolith",
    "Old Growth", "Thornmaiden", "Eclipse", "Apex Predator", "Greenfather",
}

lines = text.splitlines()
units = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if (
        line
        and len(line) < 40
        and i + 2 < len(lines)
        and "ap.tft.tools/img/general/gold" in lines[i + 2]
    ):
        name = line
        m = re.search(r"(\d+)!", lines[i + 2])
        cost = int(m.group(1)) if m else None
        traits = []
        j = i + 3
        while j < len(lines) and not lines[j].strip().startswith("](/info/set-180/units/"):
            t = lines[j].strip()
            if t in KNOWN and t not in traits:
                traits.append(t)
            j += 1
        if traits:
            units.append((name, cost, traits))
        i = j
    else:
        i += 1

for name, cost, traits in units:
    print(f"{name}\t{cost}\t{', '.join(traits)}")
print("---TOTAL", len(units))
