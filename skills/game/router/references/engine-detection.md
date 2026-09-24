# Project fingerprint — Godot only

The catalog is Godot-first: there is no other engine to detect. This file records the complete
fingerprint, the version sources, and the ambiguities a fingerprint can raise.

## Fingerprint

| Signal | Meaning | Root |
|--------|---------|------|
| `project.godot` | Godot project (authoritative) | `skills/game/` |
| `*.tscn`, `*.gd`, `*.gdshader`, `*.tres`, `export_presets.cfg` | Godot project, weaker signal | `skills/game/` |

`project.godot` wins over any other file. If it is absent but Godot files are present, the project
is still Godot — the signals are complementary, never exclusive.

## Version

Read the version before using version-sensitive APIs:

| Source | What it gives |
|--------|---------------|
| `config/features` in `project.godot` | the feature set the project was saved with |
| project documentation / toolchain config | the pinned editor or export template |
| `godot --version` on the local machine | the installed binary, useful to confirm |

The catalog targets Godot 4.x as a whole, 2D and 3D. An existing project keeps its own pinned
version; a migration is a deliberate, explicit request, never a default.

## Ambiguities

- **A `.csproj` inside a Godot project.** The project is still Godot. Route GDScript work to
  `godot-gdscript`; there is no curated C# skill (see `docs/adr/0002-gdscript-first.md`).
- **Several projects in one repository.** Route by the file or subdirectory the request is about.
  If it is still ambiguous, ask one targeted question.
- **No Godot files at all.** The request is either concept-level (no engine needed) or about a
  project that isn't here yet. Ask one targeted question, then default to Godot.
- **The repository itself.** This repository is the skill system, not a game: a request about
  editing skills is not a game-development request, so don't route it.

## Signals that are not engines

These files sharpen the **phase**, never the engine:

| File / cue | Phase |
|------------|-------|
| `export_presets.cfg` | publish |
| `steam_appid.txt` | publish (Steam) |
| `.itch.toml`, a `butler` command | publish (itch.io) |
| a `prototype/` folder at the project root | prototype |
