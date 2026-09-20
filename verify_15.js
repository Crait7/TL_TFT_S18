// Quick verify: extract core logic test for 11 slots + any2 emblems
// Minimal port of evaluate + known best board
const UNIQUE = new Set(["Attuned","Avatar","Bounty Seeker","Emerald Aspect","Monolith","Old Growth","Thornmaiden","Caustic","Greenfather","Apex Predator"]);
const BP = {Adaptor:2,Brawler:2,Defender:2,Executioner:2,Hunter:2,Invoker:2,Juggernaut:2,Rapidfire:2,Ravager:2,Spellweaver:2,Summoner:2,Vanguard:2,Blossom:3,Coven:3,Elderwood:3,Blackthorn:2,Fae:2,"Flora Fatalis":1,Inferno:2,Lunar:2,Primal:2,Riftbeast:3,Solar:3,Sprykin:3,Rival:1};
const U = {
  Pebbles:[1,["Riftbeast","Invoker"],1],
  Fiddlesticks:[3,["Flora Fatalis","Defender","Spellweaver"],1],
  Sentinel:[4,["Riftbeast","Vanguard","Invoker"],1],
  "Mama Beak":[3,["Riftbeast","Summoner","Rapidfire"],1],
  Azir:[3,["Blackthorn","Executioner","Summoner"],1],
  Veigar:[1,["Blackthorn","Sprykin","Spellweaver"],1],
  Diana:[3,["Lunar","Ravager","Vanguard"],1],
  Aphelios:[4,["Lunar","Rapidfire"],1],
  Akali:[1,["Inferno","Adaptor","Ravager"],1],
  Kennen:[5,["Inferno","Executioner"],1],
  Lillia:[4,["Fae","Defender"],1],
};
const team = ["Pebbles","Fiddlesticks","Sentinel","Mama Beak","Azir","Veigar","Diana","Aphelios","Akali","Kennen","Lillia"];
const counts = {};
for (const t of Object.keys(BP)) counts[t]=0;
for (const n of team) {
  for (const t of U[n][1]) if (!UNIQUE.has(t)) counts[t]++;
}
// emblems
counts.Adaptor++; counts.Fae++;
const act = Object.keys(BP).filter(t => counts[t] >= BP[t]);
console.log("slots", team.length);
console.log("counts", counts);
console.log("activated", act.length, act);
console.log("expect 15:", act.length === 15 ? "PASS" : "FAIL");
