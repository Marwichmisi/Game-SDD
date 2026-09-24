# Research #4 — Capacités Godot-MCP : opérations, prérequis et rôle normatif

Part of #1. Question : que sait faire exactement `IvanMurzak/Godot-MCP`
(inspecter arbre de scène, créer/modifier nodes, lancer play-test, lire erreurs debugger,
prérequis Godot 4.x, config, limites) et quel rôle normatif lui donner dans la spec
(opérations obligatoires par phase, fallback CLI `godot --headless` sans MCP,
GDScript first / C# en variante) ?
Contexte : Q3+Q8 validés (Godot 4.x 2D+3D, MCP obligatoire + fallback).
Ne configure pas le MCP, établit les faits. Ne ferme pas #4.

Date : 2026-09-24. Sources primaires uniquement (README + `cli/README.md` +
`docs/ARCHITECTURE.md` + `docs/runtime-security.md` du repo Godot-MCP,
doc officielle Godot CLI). Aucune installation ni test local effectués.

## 1. Ce qu'est Godot-MCP (faits)

- Addon C# **éditeur** (`addons/godot_mcp/`, `EditorPlugin` `[Tool]`) qui expose des
  opérations éditeur comme **AI Tools** et les relie à un serveur MCP via le backend
  cloud partagé `https://ai-game.dev` (même backend que Unity-MCP) ou un serveur
  auto-hébergé. La stack MCP/réflexion n'est pas forkée : consommée depuis nuget.org
  en `PackageReference` (`com.IvanMurzak.ReflectorNet`, `com.IvanMurzak.McpPlugin`).
- **42 outils intégrés en 12 familles** (noms miroir Unity-MCP : `scene-*`, `node-*`…).
  Tout outil éditeur est disponible dès l'addon activé, sans config supplémentaire,
  et retourne un résultat structuré sérialisé ReflectorNet (ou PNG pour screenshots).
  Exceptions : `ping` + `godot-skill-*` sont des **system tools** (surface HTTP
  `/api/system-tools/`, non annoncés en `tools/list`) ; `runtime-errors-*` concerne le
  **jeu en cours d'exécution** et est **OFF par défaut** (opt-in
  `builder.WithRuntimeErrorCapture()`).
- Architecture : Godot compile **tous les `.cs` du projet en un seul assembly** ;
  le code éditeur est exclu du jeu exporté par `#if TOOLS` (Debug = éditeur avec
  `TOOLS` ; `ExportDebug`/`ExportRelease` = sans). Règle : `Editor/` peut référencer
  `Runtime/`, jamais l'inverse en code shippé (garde CI
  `scripts/check-runtime-boundary.py`). Les 7 familles éditeur
  (`node, scene, resource, filesystem, script, screenshot, editor`) sont `#if TOOLS`
  et **n'existent pas** dans un build exporté.

## 2. Prérequis (normatif pour la spec)

| Prérequis | Fait source |
| --- | --- |
| **Godot 4.3+ édition mono (C#/.NET)** — floor `Godot.NET.Sdk/4.3.0` ; 4.4/4.5 OK | README § Requirements |
| Build **standard (GDScript-only) exclu** : ne peut pas compiler l'addon | README IMPORTANT |
| **.NET 8 SDK** (`net8.0`) | README § Requirements |
| **Node.js `^20.19.0 \|\| >=22.12.0`** pour `godot-cli` (npm `godot-cli`) | `cli/README.md` |
| 2 `PackageReference` **pinnés exacts** : `com.IvanMurzak.ReflectorNet 5.4.1` + `com.IvanMurzak.McpPlugin 8.6.0`, **plus** `<EmbeddedResource Include="addons/godot_mcp/extensions.catalog.json" LogicalName="Godot-MCP.extensions.catalog.json" />` (sans elle, panneau Extensions **vide**) ; `dotnet restore` + build | README Step 2 |
| Install addon : `godot-cli install-plugin` (télécharge le zip de release assortie, ajoute pins + catalog, active le plugin — idempotent) **ou** manuel AssetLib / zip `godot-mcp-addon-<version>.zip` / copie source, puis activer dans Project Settings → Plugins (`[Godot-MCP] plugin loaded`) | README Quick Start + Step 1 |
| Auth cloud : `godot-cli login` (OAuth 2.1 device flow RFC 8628, credential machine `~/.ai-game-dev/credentials.json`, auto-adopté par le plugin ; aucun PAT) ; `GODOT_MCP_TOKEN` en override manuel CI/headless | README § Connect |
| `godot-cli open` **builde d'abord** (`dotnet build --configuration Debug`) sinon Godot désactive l'addon au premier open (`Unable to load addon script…`) ; projets GDScript-only (sans `.csproj`) = no-op ; `--no-build` pour sauter | `cli/README.md` (`open`/`build`) |
| Résolution binaire éditeur : `--editor-path` > `GODOT_BIN`/`GODOT4_BIN` > `PATH` (mono préféré sous Windows) > chemins d'install usuels par OS | `cli/README.md` |

## 3. Opérations : les 12 familles (42 outils)

| Famille | Outils | Couvre le besoin spec ? |
| --- | --- | --- |
| `node` (7) | `node-find`, `node-create` (avec `index` fratrie, instanciation `.tscn`), `node-modify`, `node-set-parent`, `node-reorder` (`MoveChild`), `node-duplicate`, `node-delete` | **Inspecter + créer/modifier l'arbre de scène : oui** (via `EditorInterface`, main thread) |
| `scene` (5) | `scene-open`, `scene-save`, `scene-create`, `scene-list-opened`, `scene-get-data` | **Ouvrir/sauver/créer/inspecter `.tscn` : oui** |
| `resource` (6) | `resource-find`, `resource-get-data`, `resource-modify`, `resource-create`, `resource-move`, `resource-delete` (via `ResourceLoader/Saver`, `.import` cohérents) | **Muter `.tres`/`.res` : oui** |
| `filesystem` (2) | `filesystem-list` (arborescence `res://`, types + uids via `EditorFileSystem`), `filesystem-reimport` | **Parcourir/réimporter : oui** |
| `script` (6) | `script-read/create/update/delete`, `script-attach-to-node`, `script-validate` (diagnostics parse/compile **GDScript** structurés) | **CRUD `.cs` + `.gd`, attacher, valider GDScript : oui** |
| `screenshot` (3) | `screenshot-viewport`, `screenshot-camera`, `screenshot-isolated` (PNG inspectable par LLM) | **Feedback visuel : oui (éditeur)** |
| `editor` (4) | `editor-application-get-state`, `editor-application-set-state` (**start/stop du jeu**, qui tourne dans un **processus séparé**), `editor-selection-get/set` | **Play-test start/stop + sélection : oui ; pas de step frame** |
| `console` (2) | `console-get-logs` (logs collectés `GD.Print/PushWarning/PushError` + diagnostics connexion), `console-clear-logs` | **Lire erreurs éditeur : oui** |
| `reflection` (2) | `reflection-method-find/call` (toute méthode C#, public/privé, tous assemblies via ReflectorNet) | **Échappatoire C# : oui** |
| `runtime-errors` (2) | `runtime-errors-get` (page newest-kept `{sequence,message,type,source,file,line,function,stackTrace,frames,timestamp}`, poll incrémental `sinceSequence`, `available:false` si jamais activé), `runtime-errors-clear` | **Lire erreurs du jeu en cours : oui, si opt-in code** |
| `ping` (1, système) | `ping` (sonde readiness éditeur→SignalR→dispatch, via `/api/system-tools/ping` ou `godot-cli run-system-tool ping` / `wait-for-ready`) | **Santé : oui (hors `tools/list`)** |
| `skills` (2, système) | `godot-skill-create` (nouvel outil C#, callable après rebuild), `godot-skill-generate` (régénère `SKILL.md`) | **Extension outillage : oui, C# only** |

Points de vigilance : tout appel Godot API doit passer par le main thread
(`MainThread.Instance.Run(...)`) ; `godot-skill-create` exige un rebuild C#
(Godot compile le C# hors-bande) ; `setup-skills` CLI génère localement depuis un
catalogue intégré (pas besoin d'éditeur live), contrairement au path éditeur.

## 4. Play-test & debugger : ce qui est couvert, ce qui ne l'est pas

- Start/stop jeu : `editor-application-set-state` ; lecture état : `editor-application-get-state`.
- Logs éditeur : `console-get-logs` (filtres) / `console-clear-logs`.
- Erreurs GDScript **parse** : `script-validate`.
- Erreurs **runtime du jeu en cours** : uniquement via `runtime-errors-get/clear` **après**
  opt-in explicite dans le code du jeu (`GodotMcpRuntime.Initialize(b =>
  b.WithRuntimeErrorCapture())` + `Connect()` depuis un autoload `_Ready()`).
  Canaux : (1) flux moteur Godot 4.5+ (`OS.AddLogger` : erreurs runtime GDScript,
  `push_error/warning`, shaders, avec origine `file/line/function` + backtrace
  multi-frame `frames`/`stackTrace` sur 4.5+) ; (2) `AppDomain.UnhandledException` ;
  (3) `TaskScheduler.UnobservedTaskException` (observé sans `SetObserved()`).
  **Dégradation : sur Godot < 4.5, pas de hook `OS.AddLogger` managé** → canal moteur
  indisponible (stub no-op), canaux C# toujours actifs ; sans opt-in, `available:false`
  (une liste vide ne doit jamais être lue comme « sain »).
- **Non couvert par MCP** : pas de breakpoints/step/LOD debugger via outils ; le protocole
  Godot (`--remote-debug`, `--dap-port` GDScript DAP, `--lsp-port`) existe côté moteur
  mais n'est exposé par **aucun** outil MCP. Preuve visuelle d'exécution : screenshots.
- Sécurité runtime (contrat `docs/runtime-security.md`) : runtime **default-OFF**
  (zéro outil tant que non enregistré, `Connect()` explicite, familles éditeur
  non compilées donc non enregistrables) ; exiger **loopback + token**
  (`GODOT_MCP_HOST=http://localhost:…`, `AuthOption=token`, token via
  `GODOT_MCP_TOKEN` plutôt qu'en dur) ; `WithRuntimeErrorCapture()` seulement sur
  connexion de confiance (messages + stack traces complètes exposés à l'agent).
  Côté éditeur : config persistée **plaintext** `user://godot-mcp-config.json`
  (hypothèse : compte local de confiance) ; pont dev-control HTTP non authentifié
  mais **éditeur-only + loopback + gate `GODOT_MCP_DEV_CONTROL=1`**.

## 5. Connexion & CLI (faits pour écrire la spec)

- Modes : **Cloud (défaut)** `https://ai-game.dev` (`/mcp` ajouté auto) vs **Custom**
  (serveur propre, défaut `http://localhost:8080`). Env :
  `GODOT_MCP_CONNECTION_MODE` (Cloud/Custom, insensible à la casse),
  `GODOT_MCP_CLOUD_URL`, `GODOT_MCP_HOST`, `GODOT_MCP_TOKEN` (quotes trimmées),
  `GODOT_MCP_AUTH_OPTION`, `GODOT_MCP_LOG_LEVEL`. L'env **prime toujours** sur la
  config sérialisée (utile CI/headless) ; `godot-cli open` les propage via flags.
- Commandes CLI utiles : `open` (build + `--editor --path` + env), `build`,
  `run-tool <tool>` (POST `<base>/api/tools/<tool>`), `run-system-tool`
  (`/api/system-tools/`, dont `ping`), `status`, `wait-for-ready` (poll `ping`),
  `login`, `setup-mcp <agent>` (config agent, URL pinnée `<host>/mcp/p/<pin>` par
  projet + project key `agd_pk_…`, `--no-pin/--oauth/--regenerate-key`),
  `setup-skills`, `configure` (`.godot-mcp/features.json`), `close`, `install-plugin`,
  `install-extension` (catalogue **actuellement vide** : tout id inconnu),
  `remove-plugin`, `update`.
- Résolution URL serveur (`run-tool/status/wait-for-ready`) : `--url` >
  `GODOT_MCP_HOST` > `GODOT_MCP_CLOUD_URL` (+`/mcp`) > Cloud défaut >
  marqueur projet `.ai-game-dev/project.json` > fallback local
  `http://localhost:<port-dérivé>`.
- Serveur auto-hébergé : binaire partagé `gamedev-mcp-server` (repo séparé,
  version **pinnée** par constante `ServerVersion`), téléchargeable par l'addon
  (HTTPS github.com only, `gamedev-mcp-server-<rid>.zip`, 7 RIDs, cache
  `.godot/mcp-server/<rid>/`, match exact, **sauté sous CI** `CI/GITHUB_ACTIONS`)
  ou manuel (`--client-transport streamableHttp|stdio`, Docker
  `aigamedeveloper/mcp-server`) ; `stdio` = client lance le binaire, `streamableHttp`
  = process standalone/cloud.

## 6. Fallback CLI `godot --headless` sans MCP (doc officielle Godot)

Source : `docs.godotengine.org`, Command line tutorial (stable). `--headless` =
`--display-driver headless --audio-driver Dummy`, tous builds. Recettes fallback :

```bash
godot --headless --path <projet> --import                                  # import ressources puis quit (implicite --editor --quit)
godot --headless --path <projet> --check-only --script res://outil.gd      # parse-only, quit (avec --script)
godot --headless --path <projet> -s res://batch.gd                         # script SceneTree/MainLoop (batch import/export)
godot --headless --path <projet> --export-release "<preset>" <sortie>      # export CI (templates requis) ; --export-debug/--export-pack variantes
godot --headless --path <projet> --build-solutions                         # build solutions C# (implicite --editor)
godot --headless --path <projet> <scene>.tscn --quit-after 600             # run une scène N frames puis quit (smoke test)
godot --headless --path <projet> -d <scene>.tscn                           # debugger stdout local
```

Notes : `--path` requis hors cwd projet ; preset d'export doit matcher
`export_presets.cfg` ; `--headless` **requis** sans GPU (CI) et évite la fenêtre sinon ;
`--quit`/`--quit-after` bornent les runs.

## 7. GDScript first / C# variante (faits)

- `script-*` lit/crée/met à jour **`.cs` ET `.gd`**, attache les deux aux nodes ;
  seule la **validation** (`script-validate`) est GDScript-spécifique.
- En revanche : l'addon lui-même est **C#** (mono obligatoire même pour un projet
  100 % GDScript dès qu'on veut MCP), `reflection-*` et `godot-skill-create` sont
  **C# only**, et les outils custom (`[AiToolType]/[AiTool]`) s'écrivent en C#.
- Position normative proposée : **GDScript first** pour le code jeu des phases
  (lisible, `script-validate` + `--check-only` en fallback), **C# en variante**
  quand le ticket l'exige (perf, interop, outil custom, reflection) ; tout outil
  custom MCP reste C# par construction.

## 8. Limites connues (à inscrire dans la spec comme contraintes)

1. Mono-only : build GDScript-only inutilisable avec MCP.
2. Pins NuGet + `EmbeddedResource` exacts requis, sinon non-compilation / Extensions vide.
3. Premier `open` sans build = addon désactivé ; CI sans `dotnet build` préalable = échec.
4. Le jeu tourne dans un **processus séparé** : MCP pilote le cycle de vie, pas le pas-à-pas.
5. `runtime-errors` exige du code opt-in **dans le jeu** ; backtrace profonde GDScript
   seulement en 4.5+ ; moteur < 4.5 = canal C# seul.
6. Screenshots = éditeur (viewport/caméra/node isolé), pas de capture générique du binaire exporté.
7. Pas de breakpoints/step via MCP ; DAP/LSP Godot non exposés.
8. Serveur local auto-téléchargé : réseau github.com + version pinnée requis, sauté en CI.
9. Catalogue d'extensions vide : `install-extension` sans effet utile à ce jour.
10. AssetLib : entrée modérée, peut être invisible → zip de release ou copie source.
11. Config éditeur persistée en clair ; dev-control non authentifié mais gaté (ne pas
    confondre avec une surface prod).

## 9. Rôle normatif proposé pour la spec (opérations obligatoires par phase)

| Phase (spec Game-SDD) | MCP obligatoire | Preuve attendue | Fallback sans MCP |
| --- | --- | --- | --- |
| Setup projet | `ping` (via `wait-for-ready`), `filesystem-list` | `pong` + listing `res://` | `godot --headless --path . --import` + `--version` |
| Création scène | `scene-create`, `node-create/find`, `scene-save`, `scene-get-data` | `.tscn` sauvé + structure relue | fichiers `.tscn` versionnés + `--import` OK |
| Scripting | `script-create/update/read`, `script-attach-to-node`, `script-validate` (GDScript) | diagnostics vides + attachement vérifié (`node-find`) | `godot --headless --check-only --script` + `-s` batch |
| Play-test | `editor-application-set-state` (start/stop), `screenshot-viewport/camera`, `console-get-logs` | screenshots + logs sans erreur | `godot --headless <scene> --quit-after N` + log stdout |
| Debug runtime | `runtime-errors-get` (`sinceSequence`), `runtime-errors-clear` (si opt-in compilé) | `available:true`, page vide ou séquences traitées | run `-d`, lire stderr/stdout, corriger, rejouer |
| Itération | `node-modify/set-parent/reorder/duplicate/delete`, `resource-*`, `filesystem-reimport`, `editor-selection-*` | relecture `scene-get-data`/`resource-get-data` après chaque mutation | édition fichiers + `--import`/`--build-solutions` |
| Santé/porte | `ping` avant chaque lot d'appels ; `status` en diagnostic | `pong` systématique | code retour CLI `godot` == 0 |

Règles transverses proposées : (a) MCP **obligatoire** quand l'éditeur est pilotable,
fallback `godot --headless` **autorisé et documenté** sinon (CI sans GPU, MCP indisponible) ;
(b) **GDScript first**, C# en variante (cf. §7) ; (c) runtime-error capture opt-in seulement
sur connexion de confiance loopback+token ; (d) `ping`/`skills` reconnus comme system tools
(non `tools/list`) dans les procédures.

## 10. Sources

- README Godot-MCP (Tools Reference, Requirements, Installation, Connect, Server setup,
  Customize Tools, Runtime usage, Capturing in-game runtime errors) :
  `https://github.com/IvanMurzak/Godot-MCP` (raw :
  `https://raw.githubusercontent.com/IvanMurzak/Godot-MCP/main/README.md`).
- CLI : `https://github.com/IvanMurzak/Godot-MCP/blob/main/cli/README.md`
  (raw `.../main/cli/README.md`) — `open/build/run-tool/run-system-tool/status/wait-for-ready/
  login/setup-mcp/setup-skills/install-plugin/install-extension`, résolution éditeur et URL.
- Architecture éditeur vs runtime : `docs/ARCHITECTURE.md`
  (raw `.../main/docs/ARCHITECTURE.md`) — un seul assembly, `#if TOOLS`, règle Editor→Runtime, garde CI.
- Contrat sécurité runtime : `docs/runtime-security.md`
  (raw `.../main/docs/runtime-security.md`) — opt-in, zéro outil par défaut, env `GODOT_MCP_*`,
  token plaintext `user://godot-mcp-config.json`, dev-control gaté.
- Godot officiel, Command line tutorial :
  `https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html`
  (`--headless`, `--import`, `--check-only`, `--script`, `--export-*`, `--build-solutions`,
  `--quit/--quit-after`, `-d`, `--path`).
