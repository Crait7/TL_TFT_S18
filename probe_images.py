# -*- coding: utf-8 -*-
import urllib.request, ssl
ctx = ssl.create_default_context()

def check(url):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            return r.status, r.headers.get("Content-Type",""), r.headers.get("Content-Length","")
    except Exception as e:
        return "ERR", str(e)[:60], ""

missing = {
    "Varus":"varus","Caitlyn":"caitlyn","LeBlanc":"leblanc","Sejuani":"sejuani",
    "Teemo":"teemo","Warwick":"warwick","Cassiopeia":"cassiopeia","Diana":"diana",
    "Hecarim":"hecarim","Kog'Maw":"kogmaw","Master Yi":"masteryi","Rammus":"rammus",
    "Rengar":"rengar","Ahri":"ahri","Amumu":"amumu","Ezreal":"ezreal","Sivir":"sivir",
    "Zyra":"zyra","Lux":"lux"
}
alts = []
for key, slug in missing.items():
    alts += [
        (key, f"https://raw.communitydragon.org/latest/game/assets/characters/{slug}/hud/{slug}_square.png"),
        (key, f"https://raw.communitydragon.org/latest/game/assets/characters/{slug}/hud/{slug}_square_0.png"),
        (key, f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/{slug}/hud/{slug}_square.png"),
        (key, f"https://raw.communitydragon.org/latest/game/assets/characters/{slug}/hud/{slug}_circle.png"),
        (key, f"https://ddragon.leagueoflegends.com/cdn/14.1.1/img/champion/{slug.capitalize()}.png"),
        (key, f"https://ddragon.leagueoflegends.com/cdn/14.1.1/img/champion/{slug}.png"),
        (key, f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{slug.capitalize()}_0.jpg"),
        # tactics.tools face
        (key, f"https://ap.tft.tools/img/gg17/face/da_18_{slug}.jpg"),
        (key, f"https://ap.tft.tools/img/gg17/face/da_18_{slug}_ad.jpg"),
        (key, f"https://ap.tft.tools/img/gg17/face/da_{slug}18.jpg"),
        (key, f"https://ap.tft.tools/img/gg17/face/da_{slug}18_ap.jpg"),
    ]

# special TFT units faces from tactics.tools (known good names)
tft_faces = [
    ("Pebbles", "https://ap.tft.tools/img/gg17/face/da_18_sentry.jpg"),
    ("Cinderling", "https://ap.tft.tools/img/gg17/face/da_cinderling18.jpg"),
    ("Gromp", "https://ap.tft.tools/img/gg17/face/da_gromp18_ap.jpg"),
    ("Murkwolf", "https://ap.tft.tools/img/gg17/face/da_murkwolf18.jpg"),
    ("Scuttlecrab", "https://ap.tft.tools/img/gg17/face/da_scuttlecrab18.jpg"),
    ("Krug", "https://ap.tft.tools/img/gg17/face/da_krug18.jpg"),
    ("Mama Beak", "https://ap.tft.tools/img/gg17/face/da_crimsonraptor18.jpg"),
    ("Brambleback", "https://ap.tft.tools/img/gg17/face/da_brambleback18.jpg"),
    ("Sentinel", "https://ap.tft.tools/img/gg17/face/da_sentinel18.jpg"),
    ("Elder Dragon", "https://ap.tft.tools/img/gg17/face/da_18_elderdragon.jpg"),
    ("Kobuko", "https://ap.tft.tools/img/gg17/face/da_18_kobuko.jpg"),
    ("Yunara", "https://ap.tft.tools/img/gg17/face/da_18_yunara.jpg"),
    ("Alune", "https://ap.tft.tools/img/gg17/face/da_18_alune.jpg"),
    ("Lux Fae", "https://ap.tft.tools/img/gg17/face/da_18_lux_fae.jpg"),
    ("Lux Primal", "https://ap.tft.tools/img/gg17/face/da_18_lux_primal.jpg"),
    ("Lux Coven", "https://ap.tft.tools/img/gg17/face/da_18_lux_coven.jpg"),
    ("tft18_lux cdragon", "https://raw.communitydragon.org/latest/game/assets/characters/tft18_lux/hud/tft18_lux_square.png"),
    ("tft18_raptor cdragon", "https://raw.communitydragon.org/latest/game/assets/characters/tft18_raptor/hud/tft18_raptor_square.png"),
    ("tft18_elderdragon cdragon", "https://raw.communitydragon.org/latest/game/assets/characters/tft18_elderdragon/hud/tft18_elderdragon_square.png"),
    ("tft18_alune cdragon", "https://raw.communitydragon.org/latest/game/assets/characters/tft18_alune/hud/tft18_alune_square.png"),
]

print("=== missing champs alternatives ===")
found = {}
for key, url in alts:
    st, ct, cl = check(url)
    if st == 200:
        print("OK", key, url, ct, cl)
        found.setdefault(key, url)

print("\n=== tft faces / cdragon ===")
for name, url in tft_faces:
    st, ct, cl = check(url)
    print(("OK" if st==200 else "NO"), name, st, cl, url)

print("\nFound for missing:", {k:v for k,v in found.items()})
print("Still missing:", [k for k in missing if k not in found])
