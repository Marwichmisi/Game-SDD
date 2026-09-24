# Tri du noyau mattpocock — keep / adapt / drop pour SDD Godot

Ticket : `Part of #1`, wayfinder:research #2 — « Tri du noyau mattpocock ».
Branche : `research/tri-noyau`, fichier : `research/tri-noyau.md` (aucune convention `research/` existante dans le repo — emplacement sensible par défaut, signalé ici conformément au skill `research`).
Statut : décision seule, aucune implémentation (ne pas fermer #2, fermeture en session wayfinder dédiée).

## Sources primaires (toutes locales)

- `skills/engineering/*/SKILL.md` (38 skills lus en tête + frontmatter `name`/`description`) + fichiers compagnons cités (`PHASE-BOUNDARIES.md`, `DEEPENING.md`, `LOGIC.md`/`UI.md`, `tests.md`/`mocking.md`, `template.sh`, `AGENT-BRIEF.md`, `SKILL-MECHANICS.md`).
- `skills-lock.json` (39 entrées : 38 noyau + `skill-creator` hors noyau, source `anthropics/skills`).
- `.agents/skills/` (miroir des 38 + `skill-creator/`).
- `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`, `AGENTS.md`.
- Carte #1 (via `gh api`) : destination = spec SDD Godot 4.x 2D+3D, GDScript first, noyau conservé/adapté + couche jeu curatée + pilotage `IvanMurzak/Godot-MCP`, MCP obligatoire avec fallback `godot --headless`.

## Critères réutilisables pour la spec

| # | Critère | Test |
|---|---------|------|
| C1 | Godot-first / pas de stack web imposée | Le skill fonctionne-t-il sans `npm`/`pnpm`, `dependency-cruiser`, `husky`, `Prettier`, `Claude Code` ? Sinon → adapt ou drop. |
| C2 | Couverture du workflow jeu | Sert-il idée → spec → tickets → implémentation → playtest/tuning → review/export ? Sinon → périphérique. |
| C3 | SDD-compat (seams Godot) | Produit-il des seams testables Godot (scène, autoload, signal/groupe, ressource) plutôt que `index.ts`/`lib/`/`tests/` ? Sinon → adapt. |
| C4 | Non-redondance | Est-il déjà couvert par `skills/game/` (44 skills) ou par les opérations Godot-MCP ? Si oui → drop ou renvoi. |
| C5 | Leverage vs coût contexte | Routeur/vocabulaire léger et transversal → keep ; mécanisme lourd mono-stack → drop. |
| C6 | GDScript first, 2D+3D sans bridage | Exemples et checks transposables aux deux dimensions sans réécriture ? Sinon → adapt avec surcharge `game-*`. |

Règle d'application : **keep = pin intact via `skills-lock.json`** (ne pas éditer `skills/engineering/`) ; **adapt = wrapper/surcharge dans `skills/game/game-*` + conventions dans le ticket workflow #7**, jamais de fork du noyau ; **drop = exclu de la spec**, réimport explicite seul recours.

## Décision : 15 keep / 11 adapt / 12 drop (= 38)

### KEEP — intacts (15)

| Skill | Pourquoi (C) | Source |
|-------|--------------|--------|
| `grilling` | Primitive d'interview (rounds, frontier) ; Notes carte #1 : à consulter chaque session ; agnostique | `skills/engineering/grilling/SKILL.md` |
| `grill-with-docs` | Entrée du main flow avec paper trail `CONTEXT.md`/ADR ; cœur SDD | `skills/engineering/grill-with-docs/SKILL.md` (+ `ask-matt/SKILL.md` § main flow) |
| `grill-me` | Même interview, stateless, hors working-directory ; coût nul | `skills/engineering/grill-me/SKILL.md` |
| `ask-matt` | Routeur des flows (idea→ship, on-ramps, vocabulaire) ; doit pointer vers les surcharges `game-*` dans la spec | `skills/engineering/ask-matt/SKILL.md` + `PHASE-BOUNDARIES.md` |
| `domain-modeling` | Glossaire `CONTEXT.md` + ADR ; Notes carte #1 chaque session ; C2/C3 directs | `skills/engineering/domain-modeling/SKILL.md` |
| `codebase-design` | Vocabulaire module/interface/seam/depth ; transposable tel quel aux scènes/nodes (module = scène) | `skills/engineering/codebase-design/SKILL.md` |
| `to-spec` | Conversation → spec, seams au plus haut ; sortie exigée par la carte | `skills/engineering/to-spec/SKILL.md` |
| `to-tickets` | Spec → tracer bullets + blocking edges ; impose le découpage vertical Godot | `skills/engineering/to-tickets/SKILL.md` |
| `research` | Fondation de ce ticket ; méthode sources primaires ; réutilisé pour #4/#5 | `skills/engineering/research/SKILL.md` |
| `triage` | Flux bugs/requests → `ready-for-agent` ; `docs/agents/issue-tracker.md` dit PR-surface = non, donc tickets seuls | `skills/engineering/triage/SKILL.md` + `AGENT-BRIEF.md` |
| `wayfinder` | Carte #1 elle-même ; décisions pas livrables ; déjà en usage | `skills/engineering/wayfinder/SKILL.md` |
| `handoff` | Portabilité inter-sessions/répertoires ; pont prototype prescrit par `ask-matt` | `skills/engineering/handoff/SKILL.md` |
| `to-questionnaire` | Décisions externes (playtesteurs, musiciens, éditeurs) ; utile jeu | `skills/engineering/to-questionnaire/SKILL.md` |
| `wait-what` | Re-pitch STE100 + langage `CONTEXT.md` ; coût une ligne | `skills/engineering/wait-what/SKILL.md` |
| `writing-for-agents` | Style guide des docs agents ; servira à écrire les surcharges `game-*` | `skills/engineering/writing-for-agents/SKILL.md` + `SKILL-MECHANICS.md` |

### ADAPT — garder le processus, réécrire checks/exemples pour Godot (11)

| Skill | Adaptation Godot exigée (détaillée ticket workflow #7) | Source |
|-------|----------------------------------------------------------|--------|
| `implement` | Remplacer `typecheck`/`full test suite` génériques par `godot --headless` (import/check) + suite GUT/GdUnit ; garder TDD-interne + commit | `skills/engineering/implement/SKILL.md` |
| `implement-spec` | Même + graphe de tâches et frontier exécutés avec runners Godot ; `context pointers` vers scènes/ADR | `skills/engineering/implement-spec/SKILL.md` |
| `tdd` | Seams = scènes/autoloads/signaux, pas `index.ts` ; `tests.md`/`mocking.md` à transposer (doubles de nodes, scènes de test) ; nommer les seams avant tout test | `skills/engineering/tdd/SKILL.md` + `tests.md`, `mocking.md` |
| `code-review` | Axes Standards+Spec conservés ; baseline Fowler + standards repo à compléter par conventions GDScript (`godot-gdscript` de `skills/game/`) ; fixed point `git diff <pt>...HEAD` inchangé | `skills/engineering/code-review/SKILL.md` |
| `prototype` | Branches LOGIC/UI conservées ; cible = scène jetable Godot (pas HTML/route URL) ; archiver sur `prototype/<nom>` comme source primaire | `skills/engineering/prototype/SKILL.md` + `LOGIC.md`, `UI.md` |
| `diagnosing-bugs` | Feedback loop = commande `godot --headless` qui rougit sur ce bug + playtest ; phases et redaction inchangées | `skills/engineering/diagnosing-bugs/SKILL.md` |
| `resolving-merge-conflicts` | Inchangé sur le processus (intent des deux côtés, jamais `--abort`), exemples `.tscn`/`.gd` à ajouter (conflits de scènes) | `skills/engineering/resolving-merge-conflicts/SKILL.md` |
| `improve-codebase-architecture` | Rapport HTML + grilling conservés ; vocabulaire `codebase-design` appliqué aux scènes (deep scene, une scène = un seam) | `skills/engineering/improve-codebase-architecture/SKILL.md` |
| `wizard` | `template.sh` conservé ; stages à écrire pour setup Godot/MCP/export/`itch-publish` au lieu de services web génériques | `skills/engineering/wizard/SKILL.md` + `template.sh` |
| `pr` | Gabarit Summary/Evidence/Merge-Danger conservé ; Evidence = captures/behavior Godot + runs headless avant/après | `skills/engineering/pr/SKILL.md` |
| `retro` | Catégories navigation/checks conservées ; environment = opencode + Godot, pas d'hypothèse `package.json`/CI web | `skills/engineering/retro/SKILL.md` |

### DROP — exclus de la spec SDD Godot (12)

| Skill | Pourquoi (C) | Source |
|-------|--------------|--------|
| `migrate-to-shoehorn` | Test-only TS (`as` → `@total-typescript/shoehorn`) ; zéro valeur GDScript (C1 KO) | `skills/engineering/migrate-to-shoehorn/SKILL.md` |
| `setup-ts-deep-modules` | `dependency-cruiser`, `src/packages`, `pnpm` ; découpage Godot = scènes/addons, pas packages npm (C1/C3 KO) | `skills/engineering/setup-ts-deep-modules/SKILL.md` |
| `scaffold-exercises` | `ai-hero-cli`, `exercises/XX/` ; pédagogie TS, pas workflow jeu (C2 KO) | `skills/engineering/scaffold-exercises/SKILL.md` |
| `setup-pre-commit` | `husky`+`lint-staged`+`prettier`+`npm run typecheck/test` ; hooks Godot (`gdformat`, headless) relèveront du ticket workflow, pas de ce gabarit (C1 KO) | `skills/engineering/setup-pre-commit/SKILL.md` |
| `git-guardrails-claude-code` | Hooks `Claude Code` (`settings.json`) bloquant `git push`/`reset --hard` ; environnement = opencode (C1 KO ; principe réimplémentable côté opencode si besoin) | `skills/engineering/git-guardrails-claude-code/SKILL.md` |
| `claude-handoff` | Lance `claude --bg` ; doublon de `handoff` générique, fournisseur-spécifique (C5 KO → garder `handoff`) | `skills/engineering/claude-handoff/SKILL.md` |
| `setup-matt-pocock-skills` | Bootstrap one-shot déjà exécuté (commit `26d228a`, `docs/agents/*.md` présents) ; archive, pas runtime (C2 KO) | `skills/engineering/setup-matt-pocock-skills/SKILL.md` |
| `loop-me` | Life-loops `workflows/*.md` personnelles ; pas de lien jeu/SDD (C2 KO) | `skills/engineering/loop-me/SKILL.md` |
| `teach` | Workspace `MISSION.md`/lessons HTML ; pédagogie générale hors SDD (C2 KO) | `skills/engineering/teach/SKILL.md` |
| `writing-beats` | Exploit éditorial (beats/journey) ; devlogs éventuels couverts par couche jeu, pas par ce noyau (C4 KO) | `skills/engineering/writing-beats/SKILL.md` |
| `writing-fragments` | Explore sans structure ; même motif (C4 KO) | `skills/engineering/writing-fragments/SKILL.md` |
| `writing-shape` | Façonnage d'articles paragraphe par paragraphe ; même motif (C4 KO) | `skills/engineering/writing-shape/SKILL.md` |

Hors périmètre de comptage : `skill-creator` (`anthropics/skills`, `skills-lock.json`) — méta-skill de création, ni noyau mattpocock ni drop ; à référencer si la spec crée des `game-*`.

## Conséquences pour la spec (renvois, pas d'implémentation)

1. Noyau pinné : 15 keep intacts via `skills-lock.json`, 11 adaptés uniquement par surcharges `skills/game/game-*` + conventions (checks `godot --headless`, GUT/GdUnit, scènes jetables, gabarit PR Godot).
2. Tickets consommateurs : architecture #6 (layout `skills/engineering/` + `skills/game/` + synchro `.agents/skills/` + `skills-lock.json`), workflow #7 (phases, MCP obligatoire/fallback CLI, Done playtest/tuning/export), curation #3 (vérifier que `skills/game/` couvre audio/UI/tuning/export pour ne pas réintroduire les drops).
3. Point ouvert assumé : `setup-pre-commit`/`git-guardrails` écartés comme gabarits web, mais le besoin (garde-fous + hooks) demeure — à respécifier Godot-side en #7, pas en réimportant les drops.
