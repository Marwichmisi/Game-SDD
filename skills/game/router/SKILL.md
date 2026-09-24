---
name: router
description: >
  Single entry point for game work in this repository: detects a Godot 4.x project, classifies the
  request into a workflow phase, and loads the minimal set of curated Couche jeu skills before
  acting. Use to make a game, prototype a mechanic, design levels, add game feel, tune
  performance, or export and publish — and to decide which skill applies when unsure. Godot-first,
  GDScript-first, 2D+3D without lock-in.
---

# Router — Game-Development Skill Dispatcher

The entry point for game-development work in this repository. It fingerprints the project,
classifies the phase of the work, names the **minimal** set of curated skills, and tells you to
read them before acting. It **dispatches and composes** — it does not re-teach engine APIs.

The catalog is deliberately small: the Noyau stays intact, and this router only ever points at
the curated Couche jeu. If a concern has no skill here, the router says so plainly instead of
inventing a name.

## When to use

- Use at the **start of any game-development request** — building, debugging, prototyping,
  designing, polishing, exporting or publishing a Godot game.
- Use when the user says "make a game", names a phase ("prototype this", "export my game"), or
  asks "which skill should I use?".

**When *not* to use:** once the right skill is loaded and the task is squarely inside it, work
from that skill — don't re-run the router every turn. Re-route only when the task **pivots** to a
new concern.

## Routing algorithm

1. **Fingerprint the project** — read `project.godot` (or a `*.tscn` / `*.gd` file). This catalog is
   Godot-only; the version comes from the project's own metadata. §1.
2. **Classify the phase** — concept, prototype, slice, production, playtest, polish, publish. §2.
3. **Resolve the minimal set** — the smallest number of curated skills that covers the request. §3.
4. **Read (progressive disclosure)** — open only the selected `SKILL.md` bodies; their
   `references/` only on demand. §4.
5. **Compose** — engine fundamentals → discipline concept → workflow. §5.
6. **State the gap** — no skill covers it? Say so, load the closest one, and name what is
   missing. Never fabricate a skill name. §6.

---

## 1. Project fingerprint

| Signal | Meaning | Skill set root |
|--------|---------|----------------|
| `project.godot` (or `*.tscn`, `*.gd`, `*.gdshader`, `*.tres`) | Godot project | `skills/game/` |

Read the version from the project metadata before using version-sensitive APIs. An existing
project keeps its pinned version unless a migration is explicitly requested; the catalog targets
Godot 4.x as a whole, 2D and 3D.

No project file at all? Ask one targeted question, then default to Godot — this repository is
Godot-first. Never adopt another engine: it has no skills here.

## 2. Phase classification

Phases are additive — a request can need a production skill and a publish workflow at once.

| Phase | Trigger cues |
|-------|--------------|
| **concept** | "what should I build", scope, one-sentence concept, pitch |
| **prototype** | "is it fun", rough it in, greybox, blockout, spike, throwaway |
| **slice** | vertical slice, MVP, production gate, "can we build this" |
| **production** | implement a validated feature, scenes, signals, data, levels |
| **playtest** | watch real players, observe, hypothesis, balancing loop |
| **polish** | game feel, juice, camera, animation, profiling, low FPS |
| **publish** | export, build, upload, itch.io, Steam, jam submission |

File signals sharpen the phase: `export_presets.cfg` → publish; `steam_appid.txt` → Steam;
`.itch.toml` or a `butler` command → itch.io; a `prototype/` folder at the project root → prototype.

## 3. Routing table (phase → curated skills)

### 3a. Socle GDScript-first — load on demand, in this order

| Need | Skill |
|------|-------|
| language, lifecycle, typing, `await`, annotations | `godot-gdscript` |
| scene tree, instancing, autoloads | `godot-nodes-scenes` |
| signals, groups, event decoupling | `godot-signals-groups` |
| custom resources, data-driven design, `ResourceLoader` | `godot-resources` |

### 3b. Disciplines and workflows — load the minimal set

| Phase / request says | Load |
|----------------------|------|
| concept, scope lock, "what should I build" | `router` itself, then the Noyau decision skills (to-spec, to-tickets) |
| prototype, "is it fun", spike, greybox, blockout | `prototype-fast` |
| slice, MVP, production gate | `prototype-fast` + `level-design` + the Noyau ticket skills |
| production: scenes, signals, data | the socle skills of §3a |
| production: hand-authored levels, pacing, metrics | `level-design` |
| polish: game feel, juice, knockback, hit-stop | `game-feel` (+ `camera-systems` for shake, `godot-animation` for tweens) |
| polish: camera follow, deadzone, orbit, first-person look | `camera-systems` |
| polish: tween, `AnimationPlayer`, `AnimationTree` | `godot-animation` |
| polish: low FPS, frame budget, pooling, batching, profiler | `performance-optimization` (+ `physics-tuning` for the step) |
| physics feel, jitter, tunneling, fixed timestep | `physics-tuning` |
| playtest, observe players, iterate on evidence | `level-design` (in-engine loop) + the Noyau/to-questionnaire decision skills |
| publish: export, presets, headless build, web export | `godot-export` |
| publish: itch.io upload | `itch-publish` (after `godot-export`) |
| publish: Steam upload | `steam-publish` (after `godot-export`) |

### 3c. Réserve — loaded only on an explicit jam request

`game-jam` is kept in the Couche jeu as a **réserve**: load it only when the user names a
competition, a deadline (48-72 h) or a submission ("game jam", "Ludum Dare", "GMTK"). It is not
part of the default route for a normal production request. It composes with `prototype-fast` (lock
scope), `godot-export` (ship a build) and `itch-publish` (submit).

## 4. Read protocol (progressive disclosure)

1. **Preloaded:** only each skill's `name` + `description` are in context. Decide from those plus
   the fingerprint — do **not** pre-read bodies.
2. **On selection:** read the body of **each chosen** `skills/game/<name>/SKILL.md` — and only
   those. Never bulk-load the whole catalog.
3. **On demand:** read a skill's bundled `references/` files only when the subtask needs that
   depth (the skill body says when).
4. **Re-route on pivot:** if the task changes (movement → export), select and read the newly
   relevant skill instead of keeping everything loaded.

Announce what you load and why, e.g.: *"Godot project detected. Loading `prototype-fast` for the
30-minute spike and `level-design` for the blockout metrics; I'll open the pacing reference only
if the question turns to difficulty curve."*

## 5. Composition rules

- **One engine set, additive concepts.** The socle owns the engine API; a discipline owns the
  portable concept; a workflow owns the process. Order: socle → discipline → workflow.
- **Ownership on overlap:** the `godot-*` skills own API and syntax; `level-design`,
  `game-feel`, `camera-systems` and `performance-optimization` own their concept and defer to the
  `godot-*` skills for code; `prototype-fast` and the publish skills own the process.
- **Hand-offs:** every routing decision points at a curated skill; never at a name outside the
  catalog. The Noyau (to-spec, to-tickets, to-questionnaire) is invoked directly from
  `skills/engineering/` — the router does not wrap it.

## 6. Gaps — be honest, do not fabricate

The curation deliberately removed several concerns from the catalog. When a request lands there,
load the closest curated skill and **state the gap plainly**, for example:

- enemy behaviour or procedural generation → no dedicated skill here; use the socle skills
  (`godot-nodes-scenes`, `godot-signals-groups`) and say the gap.
- save/load slots, dialogue trees, HUD layout, input rebinding → no dedicated skill here; use
  `godot-resources` (for data) or `godot-nodes-scenes` (for scene composition) and say what is
  missing.
- C# instead of GDScript, networking, dedicated servers → deliberately out of scope for this
  catalog; the Godot-MCP interface needs a mono build (see `docs/adr/0001-mono-requis-par-mcp.md`)
  but no C# skill is curated here; say the gap.
- 2D-specific movement, tilemaps, physics nodes, shaders, audio → not curated here; use the
  socle and `level-design`, and say the gap.

## Worked examples

| Request | Detected project | Skills loaded (in order) |
|---------|------------------|--------------------------|
| "is grappling fun?" | Godot (`project.godot`) | `prototype-fast` |
| "block out the first level with teach-then-test metrics" | Godot | `level-design` → `godot-nodes-scenes` |
| "the hit should feel punchy" | Godot | `game-feel` → `godot-animation` (+ `camera-systems` for shake) |
| "the camera should follow my player smoothly" | Godot | `camera-systems` → `physics-tuning` |
| "we drop to 30 FPS in the boss fight" | Godot | `performance-optimization` (profile first) → `physics-tuning` |
| "export for web and push to itch.io" | Godot | `godot-export` → `itch-publish` |
| "publish the same build on Steam" | Godot + `steam_appid.txt` | `godot-export` → `steam-publish` |
| "48-hour jam, scope to the clock" | Godot | `game-jam` (réserve) → `prototype-fast` |
| "make an enemy that chases the player" | Godot | `godot-nodes-scenes` + `godot-signals-groups` (gap: no AI skill curated) |

## References

- Fingerprint details, version sources, monorepo disambiguation: `references/engine-detection.md`.
- Exhaustive kept-skill triggers, phase mapping and known gaps: `references/routing-table.md`.
