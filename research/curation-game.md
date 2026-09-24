# Curation game-skills — sélection prioritaire et mapping phases (ticket #3)

**Question (Part of #1) :** parmi les 44 skills `skills/game/` (source
`gamedev-skills/awesome-gamedev-agent-skills`), lesquels retenir en priorité
(5-8 clés) et comment les mapper aux phases
concept → prototype → vertical slice → production → polish → publish ?
Recouvrements, bruit à écarter, adaptations SDD + Godot 4.x.

**Méthode :** lecture des sources primaires locales — corps complet (`SKILL.md`)
des 12 skills prioritaires (router, prototype-fast, game-jam, level-design,
game-feel, performance-optimization, godot-gdscript, godot-nodes-scenes,
godot-export, itch-publish, steam-publish, input-systems, camera-systems,
save-systems, platformer, game-ai) + frontmatter `name/description` des 44
skills + sections « When *not* to use » et « Related skills » pour les
recouvrements. Aucune source secondaire.

**Convention de dépôt :** aucun dossier `research/` n'existait ; fichier créé à
`research/curation-game.md` (emplacement demandé par le ticket parent).

## 1. Sélection : 7 clés (+ 1 réserve)

| # | Clé retenue | Fichiers | Rôle |
|---|-------------|----------|------|
| 1 | **router** | `skills/game/router/SKILL.md` | Dispatcher d'entrée : fingerprint moteur, classification tâche, composition minimale, progressive disclosure |
| 2 | **prototype-fast** | `skills/game/prototype-fast/SKILL.md` | Question unique, timebox 30-90 min, greybox, critères keep/kill, confinement du spike |
| 3 | **level-design** | `skills/game/level-design/SKILL.md` (+ exécutant `godot-tilemap`) | Blockout→jouable : métriques, critical path, pacing tension/repos, gating, playtest |
| 4 | **game-feel** | `skills/game/game-feel/SKILL.md` (+ binôme `camera-systems`, exécutant `godot-animation`) | Juice : shake, hit-stop, tween/easing, squash & stretch, knockback, feedback |
| 5 | **socle Godot GDScript-first** | `godot-gdscript`, `godot-nodes-scenes`, `godot-signals-groups`, `godot-resources` | Langage + arbre de scènes + découplage signaux/groupes + données `.tres` |
| 6 | **performance-optimization** | `skills/game/performance-optimization/SKILL.md` (+ binôme `physics-tuning`) | Profiler d'abord, budget frame-time, pooling, batching, allocations/GC |
| 7 | **export + publish** | `godot-export` (+ `itch-publish`, `steam-publish`) | Presets/headless/CI/templates, puis upload butler (itch) / SteamPipe (Steam) |
| R | **game-jam** (réserve) | `skills/game/game-jam/SKILL.md` | Scope-to-clock + soumission ; n'activer que si la couche jeu vise aussi les jams |

Pourquoi ces 7 : elles couvrent les 6 phases sans trou (voir §2), elles sont
toutes soit moteur Godot direct, soit agnostiques avec point d'accroche Godot
documenté, et leurs propres sections « When *not* to use » confirment qu'elles
ne se marchent pas dessus une fois le découpage concept/engine/genre respecté
(router §5 : *« the **engine** skill owns API/syntax; the **discipline** skill
owns the portable concept/algorithm…; the **genre** skill owns structure/glue »*,
`skills/game/router/SKILL.md`).

## 2. Mapping aux phases

| Phase | Skills mobilisés | Points d'entrée concrets (cités des sources) |
|-------|------------------|-----------------------------------------------|
| **concept** | router (§1-§2) ; game-jam §3-§4 en option | router : détection moteur (`project.godot` → set Godot) puis classification discipline/genre/workflow (`skills/game/router/SKILL.md` §1-§3). game-jam : concept en une phrase *« You [verb] to [goal] while [constraint] »* + scope-to-clock (`skills/game/game-jam/SKILL.md` §3-§4) |
| **prototype** | prototype-fast (pilote) + socle Godot (exécution) | Brief prototype : QUESTION / CORE VERB / THROWAWAY? / TIMEBOX / KEEP IF / KILL IF ; tout le non-essentiel en greybox/primitifs (`skills/game/prototype-fast/SKILL.md` Patterns §1-§2). Confinement : `prototypes/<idea>/` séparé, un « keep » autorise un REWRITE, jamais un copier-coller du spike (Patterns §4) |
| **vertical slice** | prototype-fast + level-design (§1-§5) + game-jam §5 | Boucle 30 s start→play→lose/win→restart d'abord (game-jam §5 : *« Build the vertical slice first »*). level-design : métriques perso verrouillées avant la géométrie, blockout complet, critical/golden path (`skills/game/level-design/SKILL.md` Core workflow §1-§3) |
| **production** | socle Godot + level-design (§4-§6) + disciplines à la demande via router | Socle : `godot-gdscript` (typing, lifecycle, `@export/@onready`, signaux, `await`), `godot-nodes-scenes` (composition, instanciation, autoloads), `godot-signals-groups` (découplage), `godot-resources` (données `.tres`, `ResourceLoader`). level-design : pacing, teach-then-test, gating (`skills/game/level-design/SKILL.md` §4-§6). Vague 2 à la demande : `save-systems`, `input-systems`, `game-ui-ux`+`godot-ui-control`, `game-ai`, `dialogue-systems` |
| **polish** | game-feel + camera-systems + performance-optimization + physics-tuning | game-feel pour le punch, `camera-systems` pour follow/deadzone/orbit (le skill game-feel ne fait que déclencher le shake : *« this skill only triggers the shake »*, `skills/game/game-feel/SKILL.md`). perf : *mesurer au profiler d'abord*, raisonner budget CPU-vs-GPU, puis pooling/batching/allocations (`skills/game/performance-optimization/SKILL.md`). physics-tuning : timestep fixe vs variable, interpolation, CCD anti-tunneling, jitter (`skills/game/physics-tuning/SKILL.md`) |
| **publish** | godot-export → itch-publish / steam-publish | `godot-export` : templates, `export_presets.cfg`, exports headless/CI, web COOP/COEP, builds headless (`skills/game/godot-export/SKILL.md`). Puis mécaniques d'upload : `butler push` + channels (`skills/game/itch-publish/SKILL.md`) / depots + `steamcmd` + branches (`skills/game/steam-publish/SKILL.md`). game-jam §6-§7 : réserve ~20 % de l'horloge au shipping, submit tôt |

Articulation SDD (noyau `skills/engineering/`) par phase : **concept** → `to-spec`
(synthèse conversation → spec, label `ready-for-agent`) ; **vertical
slice/production** → `to-tickets` (tranches verticales tracer-bullet + arêtes de
blocage) ; **toutes phases** → `grilling`/`grill-with-docs` pour les tickets
grilling et `prototype` (noyau engineering) si un ticket prototype émerge —
rôles rappelés dans la carte #1. Le protocole de lecture du router (§4,
*progressive disclosure* : préchargé = `name`+`description` seuls, corps des
seuls skills choisis, `references/` sur demande) s'applique tel quel aux agents
SDD pour limiter le contexte.

## 3. Recouvrements identifiés (garder les deux, avec règle de propriété)

Les skills documentent eux-mêmes la répartition ; ne pas les dédupliquer, les
composer via le router §5 (concept ↔ API moteur) :

- `game-ai` (choisir FSM/BT/steering/A*) vs `ai-behavior-trees-utility-ai`
  (implémenter le runtime BT + Utility) : le second est le *« implementation
  companion »* du premier (`skills/game/ai-behavior-trees-utility-ai/SKILL.md`,
  intro). Vague 2, pas clé.
- `game-ui-ux` (patterns agnostiques : ancres, scaling, focus, pile d'écrans)
  vs `godot-ui-control` (`Control`/`Container`/`Theme`/focus concret) :
  renvois mutuels explicites dans les deux « When *not* to use ».
- `audio-design` (bus, ducking, musique adaptative) vs `godot-audio`
  (`AudioStreamPlayer`, bus, `AudioServer`) : idem, renvois mutuels.
- `shader-programming` (pipeline, UV, GLSL/HLSL) vs `godot-shaders`
  (`.gdshader`, `canvas_item`/`spatial`, `TIME`/`UV`) : idem.
- `physics-tuning` (timestep, CCD, jitter) vs `godot-physics` (corps, layers vs
  masks, `Area`, raycasts) : *« Tuning the feel… → physics-tuning »* d'un côté,
  *« exact physics nodes… → godot-physics »* de l'autre.
- `platformer` (genre : controller run/jump + feel aids) vs `godot-2d-movement`
  (`CharacterBody2D`, `move_and_slide`) : le genre renvoie à l'API brute, le
  skill moteur renvoie au template genre. Même motif pour `card-game` /
  `visual-novel` → `godot-resources` + UI.
- `prototype-fast` vs `game-jam` : *« timed competition with a deadline…
  (use game-jam) »* vs *« throwaway experiments with no deadline (use
  prototype-fast) »* — d'où game-jam en réserve seulement.
- `performance-optimization` vs `godot-export` : le skill perf renvoie aux
  réglages build/release vers `godot-export` ; l'export renvoie la mécanique de
  publication vers `steam-publish`/`itch-publish` (pas de recouvrement réel,
  chaîne propre).

## 4. Bruit à écarter (ne pas importer en priorité)

- **Les 9 genres** (`platformer`, `roguelike`, `rpg`, `fps-shooter`,
  `tower-defense`, `card-game`, `visual-novel`, `survival-crafting`, `puzzle`) :
  templates de composition, pas de fondamentaux — le router les charge *au plus
  un par tâche* (§5) et chacun redirige vers les disciplines qu'on retient
  déjà. `platformer` reste utile comme exemple de composition
  (`godot-2d-movement` + `godot-tilemap` + `level-design` + `camera-systems` +
  `game-feel`, router §3c), pas comme clé.
- **`godot-csharp`** : cible Godot 4.x **GDScript-first** (carte #1) ; le skill
  impose le build .NET et les patterns PascalCase — à écarter sauf demande C#
  explicite. `godot-gdscript` couvre le besoin (portage 3.x→4.x : `yield`→`await`,
  `export`→`@export`).
- **`godot-multiplayer`** (ENet, `@rpc`, `MultiplayerSpawner/Synchronizer`) :
  charge réseau complète, à différer en vague ultérieure — aucun besoin multijoueur
  dans la spec carte #1.
- **`godot-3d-essentials`** en clé : à rétrograder en vague 2. La cible est
  2D+3D sans bridage, mais le socle 2D (`nodes-scenes`, `tilemap`,
  `2d-movement`) + disciplines porte le vertical slice ; la 3D s'ajoute à la
  demande via router.
- **`create-game-assets`** : dépend d'un générateur d'images (`imagegen`),
  pré-approbation de la cible visuelle, pipeline d'import — hors périmètre spec
  sans code ; différer.
- **Références non-Godot dans le router** (§1, §3a-§3b : Unity, Unreal, Bevy,
  Phaser, web-engines, Roblox, `unreal-niagara`, `unity-navmesh`…) : bruit de
  catalogue multi-moteur. À neutraliser dans l'adaptation (voir §6) : ne garder
  que la colonne Godot des tables de routage.
- **Doublons de portage 3.x→4.x** disséminés (`godot-gdscript`,
  `godot-shaders`, `godot-signals-groups`, `godot-tilemap` → `TileMapLayer`) :
  pas des skills, juste des notes à uniformiser au pin de version (§6).

## 5. Manques (les noms cités dans #3 n'existent pas tels quels)

Vérifié par recherche sur les 44 `SKILL.md` : **aucun** skill
`game-design-doc`, `vertical-slice`, `playtest-feedback` ou `balancing`
générique n'existe. Couverture partielle trouvée dans les sources :

- *Design doc* : rien de dédié → **couvert par le noyau SDD** (`to-spec` produit
  déjà Problem/Solution/User Stories/Implementation+Testing Decisions,
  `skills/engineering/to-spec/SKILL.md`). Ne pas créer de skill GDD.
- *Vertical slice* : pas de skill propre, mais `prototype-fast` (« building a
  vertical slice / MVP », When to use) + `game-jam` §5 (slice 30 s en premier)
  + `to-tickets` (tranches verticales tracer-bullet) couvrent le besoin. Ne pas
  créer de skill.
- *Playtest-feedback* : pas de skill propre ; `prototype-fast` §6-§7
  (*« Playtest immediately and honestly… one other person… kill criteria »*) +
  `level-design` §7 (*« Watch real players… Fix the blockout »*) + `game-jam`
  (H24-30 : playtest + cut). Recommandation : formaliser en **2 mini-addenda
  SDD** (grille d'observation + règle keep/kill) plutôt qu'un skill — à trancher
  dans le ticket workflow de la carte.
- *Balancing* générique : absent ; seul `tower-defense/references/balancing.md`
  (DPS vs HP vs income, targeting modes — spécifique TD) et `fps-shooter`
  §3 (time-to-kill) existent, plus `audio-design` (balance de mix, autre sens).
  Recommandation : même traitement — addendum SDD (courbes/leviers par genre),
  pas d'import.

## 6. Adaptations SDD / Godot 4.x requises

1. **Chemins** : le router suppose `skills/godot/`, `skills/unity/`…
   (`skills/game/router/SKILL.md` §1, §3a) alors que le layout validé (carte #1)
   est `skills/engineering/` + `skills/game/` (godot inclus). Réécrire les
   tables §1/§3a en `skills/game/godot-*`, ou intercaler une table de
   correspondance dans la spec.
2. **Pin de version** : tous les skills godot ciblent **Godot 4.7**
   (ex. *« Implement 2D kinematic character movement in Godot 4.7 »*,
   `skills/game/godot-2d-movement/SKILL.md`) et le router pointe un
   `../docs/VERSION-SUPPORT.md` inexistant ici. Figer le pin 4.x de la carte
   dans la spec et uniformiser les notes de portage 3.x→4.x.
3. **GDScript-first** : écarter `godot-csharp` du routage par défaut (hisser
   `godot-gdscript` + `godot-nodes-scenes` + `godot-signals-groups` en tête).
4. **Enveloppe SDD** : brancher les sorties — brief prototype/kill criteria
   (`prototype-fast` Patterns §1, §3) et décisions de level-design en entrée de
   `to-spec` ; tranches `to-tickets` alignées sur slice vertical (pas couches
   horizontales). Règles à écrire dans le ticket workflow, pas ici (pas de code
   dans cette carte).
5. **Colonne Godot seule** : purger les bindings Unity/Unreal/Roblox/web des
   tables router §3a-§3b lors de la curation (ne conserver que `godot-*` +
   disciplines agnostiques + `itch/steam-publish`).
6. **Progressive disclosure** (router §4) à reprendre comme règle d'agent SDD :
   `name`+`description` préchargés, corps à la sélection, `references/` sur
   demande — à inscrire dans la spec système.

## Sources

Sources primaires : `skills/game/*/SKILL.md` (44 fichiers, lus : corps complet
pour router, prototype-fast, game-jam, level-design, game-feel,
performance-optimization, physics-tuning, godot-gdscript, godot-nodes-scenes,
godot-export, itch-publish, steam-publish, input-systems, camera-systems,
save-systems, game-ai, ai-behavior-trees-utility-ai, platformer,
tower-defense/references/balancing.md ; frontmatter + « When not to use » pour
les 27 autres). Noyau : `skills/engineering/to-spec/SKILL.md`,
`skills/engineering/to-tickets/SKILL.md`. Carte : issue #1 (contexte, layout,
préférences). Queue de recherche : issue #3 (question).
