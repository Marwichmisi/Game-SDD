# Full routing table — curated Couche jeu

Every name here is a folder at `skills/game/<name>/SKILL.md`. This table is the exhaustive lookup
the router body summarizes: trigger words, phase, and the gaps the curation left open. There are
no other skills to load; if a concern is missing from this table, it is a gap (router body §6).

## The 7 clés

| # | Clé | Skills | Owns |
|---|-----|--------|------|
| 1 | entry point | `router` | fingerprint, phase, minimal set, gaps |
| 2 | prototype | `prototype-fast` | one question, timebox, keep/kill |
| 3 | levels | `level-design` | metrics, blockout, pacing, self-playtest |
| 4 | game feel | `game-feel`, `camera-systems`, `godot-animation` | juice, camera framing, tweens/animations |
| 5 | socle GDScript-first | `godot-gdscript`, `godot-nodes-scenes`, `godot-signals-groups`, `godot-resources` | language, scene tree, events, data |
| 6 | performance | `performance-optimization`, `physics-tuning` | profile first, frame budget, step stability |
| 7 | export + publish | `godot-export`, `itch-publish`, `steam-publish` | presets, headless builds, uploads |
| R | réserve | `game-jam` | explicit jam request only |

## Per-skill triggers

| Skill | `says:` triggers | Files |
|-------|------------------|-------|
| `router` | "which skill", "what should I use", "make a game" | — |
| `prototype-fast` | prototype, spike, "is it fun", greybox, throwaway, MVP | `prototype/` |
| `level-design` | level design, blockout, whitebox, metrics, pacing, critical path | `.tscn` with a level root |
| `game-feel` | game feel, juice, screen shake, hit-stop, knockback, squash, "make it punchy" | — |
| `camera-systems` | camera follow, deadzone, look-ahead, orbit, first-person look, camera bounds | — |
| `godot-animation` | `AnimationPlayer`, `AnimationTree`, `Tween`, blend, one-shot | `*.tscn` with animation |
| `godot-gdscript` | GDScript, `_ready`, typing, `@export`, `await`, annotations | `*.gd` |
| `godot-nodes-scenes` | scene, node tree, instancing, `PackedScene`, autoload | `*.tscn` |
| `godot-signals-groups` | signal, emit, connect, groups, decoupling, observer | `*.gd` |
| `godot-resources` | custom `Resource`, data resource, `ResourceLoader` | `*.tres` |
| `performance-optimization` | performance, low FPS, frame drops, budget, draw calls, pooling, profiler | — |
| `physics-tuning` | jitter, tunneling, fixed timestep, CCD, collision tuning | — |
| `godot-export` | export, build, presets, web export, headless export | `export_presets.cfg` |
| `itch-publish` | itch.io, `butler push`, upload build, jam submission | `.itch.toml` |
| `steam-publish` | Steam, SteamPipe, depot, store page | `steam_appid.txt` |
| `game-jam` (réserve) | game jam, 48-hour, Ludum Dare, GMTK, submission | — |

## Phase → skills

| Phase | Load |
|-------|------|
| concept | Noyau to-spec / to-tickets (direct, not wrapped) |
| prototype | `prototype-fast` (+ `godot-gdscript`, `godot-nodes-scenes` to run it) |
| slice | `prototype-fast` + `level-design` (+ socle as needed) |
| production | socle (`godot-gdscript`, `godot-nodes-scenes`, `godot-signals-groups`, `godot-resources`) + `level-design` for hand-authored spaces |
| playtest | `level-design` (in-engine loop) + Noyau decision skills; the dedicated addendum arrives with the playtest wave |
| polish | `game-feel` + `camera-systems` + `godot-animation` + `performance-optimization` + `physics-tuning` |
| publish | `godot-export` → `itch-publish` / `steam-publish` |
| jam (réserve) | `game-jam` + `prototype-fast` + `godot-export` + `itch-publish` |

## Known gaps — state them, don't invent

The curation removed these concerns from the catalog. A request that lands here gets the closest
curated skill **plus an explicit statement of the gap**:

| Concern | Closest curated skill | Gap to state |
|---------|-----------------------|--------------|
| enemy AI, behavior trees, pathfinding | `godot-nodes-scenes` + `godot-signals-groups` | no AI skill curated |
| procedural generation | `level-design` | no generation skill curated |
| save/load, persistence | `godot-resources` | no save-system skill curated |
| dialogue, branching story | `godot-signals-groups` | no dialogue skill curated |
| HUD, menus, UI layout | `godot-nodes-scenes` | no UI skill curated |
| input rebinding, gamepad, buffering | `physics-tuning` | no input skill curated |
| audio, music, mixing | `godot-animation` | no audio skill curated |
| shaders | `godot-resources` | no shader skill curated |
| 2D movement, tilemaps, physics nodes | `level-design` | no engine movement/tilemap/physics skill curated |
| C# scripting | `godot-gdscript` | C# is deliberately out of the curated catalog (see ADR-0002) |
| networking, dedicated servers | `godot-export` | networking deliberately out of scope |
| game art generation | — | asset generation out of scope |
| genre templates | `level-design` + socle | no genre skill curated; compose from the socle |
