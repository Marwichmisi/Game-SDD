# Workflows prouvés indé / petite équipe — patterns et sources à réutiliser

> Ticket source : [#5 — Workflows prouvés indé/équipe](https://github.com/Marwichmisi/Game-SDD/issues/5) (map #1).
> Statut : recherche seule — faits + sources, pas de spec. Chaque affirmation cite sa source primaire.

## 1. Scope verrouillé game-jam : un verbe, une boucle, une fenêtre de livraison

- **Règle « un verbe »** : la forme gagnante d'une jam est un seul verbe intéressant exploré un week-end, pas un petit RPG ni trois systèmes — décrire le jeu en une phrase sans « et » ; couper menu (bouton start), histoire (carton-titre), tout ce qui n'est pas le verbe, puis investir les heures gagnées dans le *feel* du verbe (*Bugnet — Your First Game Jam: A Survival Guide*, 2026).
- **Règle 1-2-3** : formalisation équivalente — 1 environnement, 2 mécaniques (hors déplacement), 3 défis ; une fois le jeu complet, interdiction d'ajouter : corriger bugs, UI, page de soumission (*1-2-3-Scope Game Jam*, itch.io).
- **Planning 48 h type** : H0–H2 idéation + plan papier ; H2–H12 boucle cœur jouable en art placeholder (si pas fun à mi-parcours avec du placeholder, simplifier, pas décorer) ; tiers médian contenu + retours (SFX tôt, pas à la fin) ; dernier quart strictement polish + build + livraison (*Bugnet*, 2026).
- **Fenêtre de livraison protégée** : les builds échouent, les uploads calent, les exports web surprennent — commencer l'export tôt ; dormir (les heures fatiguées produisent du travail négatif) (*Bugnet*, 2026).
- **Priorisation explicite Must / Should / Could / Won't** avec décisions sensibles au temps restant (outillage existant : *Game Jam Scope Board* par czhchen, itch.io).
- **Leçons de postmortems** : le jammeur vétéran Perrin Ashcroft (Locked Door Puzzle) rapporte que son erreur récurrente était de viser trop gros et de finir avec des jeux inachevés ; ce qui marche : une portée « 2 salles / 2 puzzles interconnectés » avec des endroits prévus pour couper (*Borderline Post Mortem*, Ludum Dare 51, itch.io). Retour symétrique côté équipe de 5 primo-collaborateurs : tableur de suivi, vision partagée sans « Master Designer », objectif unique « quelque chose de jouable à la fin du temps » (*A Ludum Dare Postmortem — Lessons from the Blitz*, Game Developer, 2016).
- **Écueil Godot spécifique constaté en jam** : tout marchait dans l'éditeur, tout cassait dans l'export HTML (GMTK impose le web) — curseur double, state machines à re-tester ; tester l'export tôt et souvent (*GMTK 2025 Post-Mortem — Err Friday*, itch.io).
- **Cadre institutionnel** : Global Game Jam — 48 h par fuseau horaire, équipes formées après annonce du thème, recommandation d'équipe 3–6 personnes, « fortement recommandé de ne pas dépasser 6 » (*Global Game Jam Hong Kong — Team Size* ; *globalgamejam.org/about* ; Wikipédia *Global Game Jam*). GMTK Game Jam : marathon annuel sur itch.io, dizaines de milliers de soumissions (*gamemakerstoolkit.com/jam*). Ludum Dare : Compo solo 48 h tout créé pendant l'événement vs Jam 72 h en équipe, assets tiers autorisés (*ldjam.com*, règles).

**Réutilisable SDD** : skill `game-jam` (scope-lock, planning 48/72 h, checklist export web Godot précoce) ; gabarit « phrase-sans-et » + board Must/Should/Could/Won't en entrée de prototype.

## 2. Prototypes jetables : répondre à « devons-nous faire ce jeu ? »

- **Distinction fondatrice** (Rami Ismail, Vlambeer, *Prototypes & Vertical Slice*, 2022) : les **prototypes** répondent à *« should we make this game ? »*, la **vertical slice** à *« can we make it ? »*. Confondre les deux coûte temps et argent.
- **Prototypes = placer des drapeaux dans le blob** : chaque prototype répond vite à un point d'interrogation (mécanique isolée, esquisse, kitbash, mockup, jam sonore) ; ils sont pluriels, rapides, bon marché, précis, **jetables** — ne jamais réutiliser leur code/contenu après la phase (surtout si assets d'autres jeux utilisés pour aller vite). Effets : focus (réduction de l'espace des possibles), définition (cohérence design/style), alignement d'équipe (un prototype se discute, une idée parlée reste floue et coule des projets à mi-production).
- **Cas Spelunky** : le tout premier build `EXPLORER.GMK` (un seul niveau : chauves-souris, pics, pièges à flèches) « ressemble et se joue remarquablement comme la version finale » — le cœur s'est figé très tôt ; le thème familier (spéléo/Indy) a servi de schéma reconnaissable pour que joueur et designer n'aient qu'une seule nouveauté à absorber à la fois (Derek Yu, *EXPLORER.GMK — extrait du Spelunky Book*, Game Developer, 2016 ; livre *Spelunky*, Boss Fight Books, 2016 — 222 p. sur randomisation, challenge, feedback joueur, dynamique d'équipe, finir un jeu).
- **Cas Edith Finch** : 13 histoires = 13 mécaniques inédites-mais-intuitives-sans-tutoriel, prototypées puis jetées en masse avant de souder le tout en expérience cohérente (Ian Dallas, Giant Sparrow, *Weaving 13 Prototypes into 1 Game*, GDC).
- **Tradition prototypage indé** : Kellee Santiago (thatgamecompany, Indie Fund) — gérer les hauts/bas émotionnels et financiers par prototypage itératif (*Prototyping for Innovation*, GDC) ; Mark Brown — du jam au jeu commercial en 7 mois en partant d'un prototype de jam, « impitoyable sur le scope : choisir systématiquement l'option la plus rapide », construire par couches sur fondation solide (*How I Made Word Play*, 2025).

**Réutilisable SDD** : skill `prototype-fast` (prototype = question fermée + jetable, interdiction de bâtir la prod dessus) ; règle de sortie prototype = liste de drapeaux plantés (verbes, boucle, schéma-thème).

## 3. Vertical slice : prototype *de production*, pas démo avancée

- **Définition** (R. Ismail, 2022) : construire *« one of each thing »* à fidélité proche du shipping pour traverser **tout le cycle idée→implémentation** au moins une fois et révéler les blocages de pipeline. Pour un platformer : un niveau, voire une seule section de saut difficile ; pour un shooter : une petite arène.
- **Fonction gate** : la slice décide du passage pré-production → production, en interne (sait-on faire ?) et en externe (preuve pour financeurs/recruteurs : montrer, pas raconter) — Volition l'utilise comme sas après échecs et succès passés (Greg Donovan, *The Vertical Slice Challenge*, GDC 2015).
- **Contenu type** (Nineva Studios, *Vertical Slice in Game Development*, 2026) : gameplay + art + tech + UI + audio **ensemble** au niveau qualité final, critères d'acceptation écrits **avant**, rapport de risques (prouvé / incertain / next). Durées constatées : 6–12 semaines cross-fonctionnel réduit ; erreurs classiques : trop de contenu au lieu de prouver la barre qualité, placeholder art quand le risque est visuel, perf ignorée, outils de mise à l'échelle sautés, features flatteuses non représentatives.
- **Cas Firewatch** (Campo Santo, ~10 pers., Unity) : 15 mois pour une slice représentative (art correct + vraie VO) prouvant que « marcher + parler » est intéressant, que la navigation par landmarks avec payoff narratif plaît — puis production du reste en 9 mois avec la distance « tour→lac » comme étalon (Jane Ng, *Making the World of Firewatch*, GDC 2016, slides).
- **Technique d'estimation** (R. Ismail) : après la slice, fabriquer un **deuxième** *thing* — son temps de fabrication ÷ timeline = capacité, ou × quantité voulue = estimation (avec marges). Le delta de temps slice→2ᵉ objet mesure si les correctifs pipeline ont servi.
- **Quand pitcher** (R. Ismail) : dès les prototypes + mockups/target renders (l'intérêt éditeur ne change quasiment pas entre prototype et slice — seule la croyance en capacité de production change) ; si « non » unanime, l'idée rejoint l'archive sans perdre des mois autofinancés.

**Réutilisable SDD** : phase slice explicite entre prototype et production (Q6/Q9 : prototype → slice → production), avec critères d'acceptation préalables + 2ᵉ-objet comme instrument d'estimation ; ne pas confondre slice et démo pitch.

## 4. Whitebox / blockout → jouable : garder le « cheap » jusqu'au playtest

- **Principe** (*Level Design Book — Blockout*, source primaire de référence) : le blockout (blockmesh/graybox) est un **brouillon 3D jouable** en formes simples, sans art final. « Cheap » à jeter/reconstruire vs art final « expensive » à jeter = gaspillage. On ne peut pas playtester un doc de design, **on peut playtester un blockout** (flow, balance, encounters, metrics).
- **Cinq méthodes** : primitives (cubes), brushes/modeling in-editor (contrôle max, recommandé), kit modulaire (grille + snap, télécharger un kit plutôt que fabriquer), sculpt (terrain uniquement), splines (routes/rivières). Ne pas bloquer dans Blender/Maya : pas de collision/gameplay in-engine → playtests rares (ex. : déplacer un rocher = 1 h en 6 étapes sur un AAA anonyme).
- **Boucle** : 1) sketch layout (même gribouillis) → 2) plan-sol + figurine-échelle + murs (150–200 % de la figurine, portes ≥ 2× largeur joueur) → 3) **self-playtest marché in-engine** (pas de survol éditeur : masse ? metrics ? flow ?) → 4) diverger du plan selon le playtest → 5) itérer. Problème n°1 des débutants : l'échelle (trop grand/petit) — se soigne par figurines-échelle + playtests fréquents.
- **Cas** : *Dirty Bomb — Castle* (Splash Damage) : layout → blockout aux angles simplifiés, règle « 8–12 s du spawn à l'objectif », ratio intérieur/extérieur pour viabiliser toutes les classes ; *Apex Legends — World's Edge* (Respawn, R. Reece) : rester flexible (volcan→Dôme proposé par les artistes) mais identifier le « précieux » vs le flexible (Sorting Factory intouchable).
- **Contre-cas documentés** (même source) : sur *Firewatch*, le greybox n'a répondu à aucune question — le pacing était art + narration, d'où slice art-passée directement ; sur *Untitled Goose Game*, le blockout d'imagination d'un designer jamais allé au Royaume-Uni sonnait faux — remplacé par « location scouting » (relevé photo Street View, rue Pump Street d'Orford). → Le blockout est l'outil par défaut, pas universel.
- **Outillage Godot** : addons de greyboxing Godot 4 (ex. *godot-level-block*, grid-snapped, primitives redimensionnables) ; côté Unreal : ProBuilder/SabreCSG/RealtimeCSG, CubeGrid+Modeling Tools (*Level Design Book*).
- **Référence industrie** : David Shaver & Robert Yang, *Invisible Intuition: Blockmesh and Lighting Tips* (GDC 2018) — standard actuel blockmesh + wayfinding ; Michael Markie, *Quake Mapping Tips* — exemple 5 min d'improvisation blockout→playtest→itération.

**Réutilisable SDD** : skill `level-design` (boucle sketch→blockout→self-playtest→itération, kits Godot, exceptions art-narratif documentées) ; porte de sortie blockout = playtest marché concluant.

## 5. Game-feel / juice : le fun est une accumulation de micro-décisions

- **« Juice it or lose it »** (Martin Jonasson & Petri Purho, GDC Europe 2012, Independent Games Summit) : définition canonique — *« a juicy game feels alive and responds to everything you do — tons of cascading action and response for minimal user input »* ; démo live : un clone Breakout gris bombardé d'effets couche par couche (jouable : *juicy-breakout*, sources GitHub). Références citées par les auteurs : easings de Robert Penner, *game-feel.com*, Emily Short *Make it juicy!*.
- **« The Art of Screenshake »** (Jan Willem Nijman, Vlambeer, INDIGO 2013) : ~30 micro-trucs appliqués live sur un shooter plateforme volontairement ennuyeux jusqu'à le rendre incroyable — balles plus grosses/rapides, muzzle flash, animations d'impact, knockback, shells, hitstop (~20 ms), camera kick/lerp/shake, permanence (fumée, débris), basse renforcée, mort du joueur signifiante puis balancing. Démonstration que le feel se construit **une petite décision à la fois**.
- **Cas Dead Cells** (Sébastien « deepnight » Bénard, Motion Twin, *'Dead Cells': What the F*n!?*, GDC 2019, slides) : leçon n°1 d'une équipe de 8 — les critiques parlent des **contrôles avant le gameplay** ; triches systématiques en faveur du joueur (sauts « just-in-time », correction d'arrivée — téléport/hop/climb —, double-saut d'emblée, auto-aim, free turn-around) pour ne jamais blâmer le jeu en cas de permadeath ; boucle game-over→new-game ultra-courte ; détails soignés surtout hors-challenge (« faites comme vous vous en souvenez, pas comme c'était »).
- **Accessibilité du juice** : prévoir dès le début la réduction/désactivation (motion-sickness) — Motion Twin l'a prouvé après-coup avec le patch « assist mode » 2022–2023 (continue mode, auto-hit, dégâts de pièges réglables, transparence HUD, réduction de particules, coupure du sang) (*Game Developer*, 2022–2023).

**Réutilisable SDD** : skill `game-feel` (catalogue d'effets par couches à la Jonasson/Purho + check-list Nijman + triches-contrôles à la Bénard + option accessibilité) ; passer le juice **après** boucle validée, jamais avant (cf. §1 : placeholder d'abord).

## 6. Playtest → feedback → balancing : boucle centrale, même à 1–5 personnes

- **Valve, empirisme** : le playtest comme méthode scientifique appliquée au design — observer, mesurer, décider sur preuves, pas sur opinions (Mike Ambinder, *Valve's Approach to Playtesting: the Application of Empiricism*, GDC 2009).
- **Processus in-house complet à budget** : méthode transposable AAA comme indé, aucun jeu ne s'en passe (Graham McAllister, Player Research, *Implementing an In-House Playtesting Process*, GDC Europe 2012).
- **Ultra-petites équipes** (Brian Cronin, Chugga Chugga LLC — *Slumber Realm, Monster Train, Dojo Islands* — *Playtesting Process for Ultra Small Teams*, GDC 2026, slides) : boucle **Hypothèse → session 1–5 pers. → traitement/synthèse → action (≥1, idéalement toutes les prio hautes) → retour à 1**. Précisions : tester l'expérience entière (pas seulement l'hypothèse) ; 1–5 testeurs/sprint suffisent ; consigner actions par testeur puis synthèse priorisée unique ; pistage continu des contacts/notes ; avantage indé = boucle hypothèse→action ultra-rapide (pas de process décisionnel lourd).
- **Cadence intensive** : Coin Crew Games — 200+ sessions sur *Escape Academy* (« ne jamais sauter le jour de playtest » ; jeu salué comme meilleur coop depuis *It Takes Two*) (M. Salyh & W. Bushnell, *Never Skip Playtest Day!*, Independent Games Summit, GDC).
- **Défis spécifiques indés** (Denisova et al., *Exploring Playtesting Challenges of Indie Video Game Developers*, CHI PLAY 2024 — entretiens studios de 2 à 35 pers., médiane ~10) : playtests = QA + groupes internes + salons (PAX/GDC) + démos Discord/Twitch/Reddit ; freins = ressources, recrutement, analyse des données ; besoin de démocratiser la GUR (former les non-chercheurs).
- **Recette opérationnelle** (*Game Developer — 6 steps to a successful playtesting process for an indie developer*, 2024) : 1) définir l'élément testé (contrôles, balance) sans tout tester d'un coup ; 2) démo/early-access ciblée (peu de contenu, fin intrigante) ; 3) canaux adaptés au stade (itch.io/Game Jolt/r/playmygame tôt, masse ensuite) ; 4) thèmes récurrents = vrais problèmes ; 5) équilibrer feedback vs vision (ne pas dévier sauf apport au cœur) ; 6) mises à jour agiles visibles + roadmap flexible mais tenue.

**Réutilisable SDD** : rituel playtest 1–5 pers. en boucle courte avec fiche hypothèse + synthèse priorisée (compense l'absence de skill `playtest` dédié dans `skills/game/` — **trou à combler**) ; balancing = itération sur données récurrentes, pas sur avis isolés.

## 7. Pipelines petite équipe (2–5, extensible solo–8)

| Studio / jeu | Taille & structure | Pipeline prouvé | Source |
|---|---|---|---|
| Motion Twin / *Dead Cells* | 7–8, coop sans hiérarchie (même salaire, décisions collectives) | Un jeu à la fois ; Early Access 18 mois comme showrunning (patch-notes valorisant suggestions communauté, cf. Unknown Worlds/Klei/System Era) ; scope « un peu trop gros pour nous » + permadeath comme réponse à 1 seul artiste (contenu compact) | motiontwin.com ; Bénard, GDC 2019 (slides) ; Filby & Bénard, *GamesIndustry.biz*, 2019 |
| Matt Makes Games → EXOK / *TowerFall, Celeste* | Jam → équipe resserrée, co-localisée | *TowerFall* né à la Vancouver Full Indie Jam (juin 2012, Thorson+Holowka) ; *Celeste* : jam 2015 → 300+ niveaux outillés, 2 ans ; playtests permanents en « Indie House » ; structure plate | TowerFall Wiki (development history) ; Thorson, *Designing Celeste*, GDC 2017 ; Polygon via Game Developer, 2014 |
| Mossmouth / *Spelunky* | Solo+collaborateurs (Yu + Hull) | Freeware 2008 → HD : noyau figé tôt, procédural comme multiplicateur de contenu à petite équipe, 15 conseils « finir un jeu » | Yu & Hull, *Spelunky HD Postmortem*, GDC 2011 ; Yu, *Spelunky Book*, 2016 |
| ConcernedApe / *Stardew Valley* | Solo | Itération obsessionnelle par système (ex. livre de recettes : clics min, densité d'info juste, mise en page) ; ne rien montrer à moitié cuit ; **leçon pipeline** : pas de version control au début → crash PC évité de justesse via vieux disque (sauvegardes + VCS obligatoires) | ConcernedApe, blog stardewvalley.net (juin 2026) ; PC Gamer 2016 repris juillet 2026 |
| GMTK / *Word Play* (Mark Brown) | Solo + pigistes (musique, SFX) | Jam Patreon → prototype → 7 mois, scope impitoyable (option la plus rapide), couches sur fondation, collaborateurs ciblés tard | Brown, *How I Made Word Play*, 2025 |
| Campo Santo / *Firewatch* | ~10 | Art + narration d'abord, slice de 15 mois comme étalon, landmarks narratifs au lieu de greybox | Ng, GDC 2016 |
| Coin Crew / *Escape Academy* | Petite équipe | Playtest au cœur (200+ sessions) | Salyh & Bushnell, GDC |

Constantes : **une seule chose à la fois**, équipe **3–6 max** (recommandation GGJ), décisions collectives rapides, Early Access / démos comme playtest continu, procédural et réutilisation comme multiplicateurs de contenu, VCS+sauvegardes non négociables.

## 8. Correspondance avec le SDD Godot (pistes pour la spec, sans la rédiger)

- `game-jam` ← §1 (scope-lock, planning, checklist export).
- `prototype-fast` ← §2 (questions fermées, jetable, drapeaux).
- Phase **slice** ← §3 (critères préalables, 2ᵉ-objet estimateur) — à nommer (`game-*` exact ouvert, cf. map #1).
- `level-design` (+ `godot-*` : nodes/scenes, physics, tilemap) ← §4 (blockout in-engine, metrics).
- `game-feel` (+ `physics-tuning`, `performance-optimization`) ← §5 (catalogue + accessibilité).
- **Trou : pas de skill playtest/balancing** dans `skills/game/` (44 skills scannés : rien de dédié) ← §6 à créer ou loger dans le workflow.
- Transverse : VCS/sauvegarde, « un jeu/une chose à la fois », équipe 2–5 ← §7.

## Sources (primaires d'abord)

- Ismail, R. — *Prototypes & Vertical Slice* (2022). https://ltpf.ramiismail.com/prototypes-and-vertical-slice
- Donovan, G. (Volition) — *The Vertical Slice Challenge* (GDC 2015). https://gdcvault.com/play/1022328/The-Vertical-Slice
- Ng, J. (Campo Santo) — *Making the World of Firewatch* (GDC 2016, slides). https://media.gdcvault.com/gdc2016/Presentations/Ng_Jane_MakingTheWorld.pdf
- Nineva Studios — *Vertical Slice in Game Development* (2026). https://ninevastudios.com/blog/vertical-slice-game-development-guide
- *Level Design Book — Blockout* (avec cas Dirty Bomb, Apex, Firewatch, Goose Game). https://book.leveldesignbook.com/process/blockout
- Shaver, D. & Yang, R. — *Invisible Intuition: Blockmesh and Lighting Tips* (GDC 2018). https://www.youtube.com/watch?v=09r1B9cVEQY
- Jonasson, M. & Purho, P. — *Juice It or Lose It* (GDC Europe 2012). https://www.gdcvault.com/play/1016487/Juice-It-or-Lose ; démo http://grapefrukt.com/f/games/juicy-breakout/
- Nijman, J. W. (Vlambeer) — *The Art of Screenshake* (INDIGO 2013). https://www.youtube.com/watch?v=AJdEqssNZ-U
- Bénard, S. (Motion Twin) — *'Dead Cells': What the F*n!?* (GDC 2019, slides). https://media.gdcvault.com/gdc2019/presentations/Benard-Sebastian-DeepCells.pdf ; synthèse https://www.gamedeveloper.com/design/the-secrets-of-dead-cells-smart-constraints-unlocking-the-vault-3
- Motion Twin — *worker coop / small team* . https://motiontwin.com/en ; Filby & Bénard, *GamesIndustry.biz* (2019). https://www.gamesindustry.biz/why-life-after-dead-cells-does-not-mean-growth
- Yu, D. — *Spelunky* (Boss Fight Books, 2016). https://bossfightbooks.com/products/spelunky-by-derek-yu ; extrait *EXPLORER.GMK*. https://www.gamedeveloper.com/design/explorer-gmk-an-excerpt-from-the-spelunky-book ; Yu & Hull — *Spelunky HD Postmortem* (GDC 2011). https://www.youtube.com/live/RiDy6CgBKqs ; Yu — *One More Run: Making of Spelunky 2* (GDC 2021). https://gdcvault.com/play/1027187/Independent-Games-Summit-One-More
- Thorson, M. — *Level Design Workshop: Designing Celeste* (GDC 2017). https://gdcvault.com/play/1024307 ; TowerFall dev history. http://towerfall.wikidot.com/development
- Dallas, I. (Giant Sparrow) — *Weaving 13 Prototypes into 1 Game* (GDC). https://www.gdcvault.com/play/1025016/Weaving-13-Prototypes-into-1
- Santiago, K. — *Prototyping for Innovation* (GDC). https://gdcvault.com/play/1021658/Prototyping-for-Innovation-How-to
- Cronin, B. — *Playtesting Process for Ultra Small Teams* (GDC 2026, slides). https://media.gdcvault.com/gdc2026/Slides/Cronin_Brian_PlaytestingProcessForUltraSmallTeams.pdf ; fiche https://schedule.gdconf.com/session/playtesting-process-for-ultra-small-teams/913818
- Salyh, M. & Bushnell, W. (Coin Crew) — *Never Skip Playtest Day!* (GDC). https://gdcvault.com/play/1029191/Independent-Games-Summit-Never-Skip
- Ambinder, M. (Valve) — *Valve's Approach to Playtesting* (GDC 2009). https://www.gdcvault.com/play/1566/Valve-s-Approach-to-Playtesting
- McAllister, G. (Player Research) — *Implementing an In-House Playtesting Process* (GDC Europe 2012). https://www.gdcvault.com/play/1016497/Implementing-an-In-House-Playtesting
- Denisova, A. et al. — *Exploring Playtesting Challenges of Indie Video Game Developers* (CHI PLAY 2024). https://eprints.whiterose.ac.uk/id/eprint/216480/7/CHI_PLAY_24_Indie_Playtesting_final_.pdf
- *6 steps to a successful playtesting process for an indie developer* (Game Developer, 2024). https://www.gamedeveloper.com/programming/6-steps-to-a-successful-playtesting-process-for-an-indie-developer
- Brown, M. (GMTK) — *How I Made Word Play* (2025). https://gmtk.substack.com/p/how-i-made-word-play ; https://gamemakerstoolkit.com/
- ConcernedApe — blog *Stardew Valley* (juin 2026, recipe book). https://www.stardewvalley.net/author/concernedape ; interview PC Gamer 2016 (reprise 2026, crash PC / pas de VCS).
- Global Game Jam — https://globalgamejam.org/about ; règles équipe 3–6. https://draft.ggjhk.com/ ; Ludum Dare — https://ldjam.com/ ; GMTK Jam — https://itch.io/jam/gmtk-2025
- Postmortems jam : *Borderline* (LD51). https://lockeddoorpuzzle.itch.io/borderline/devlog/438817/borderline-post-mortem ; *Second Hand* (LD35). https://www.gamedeveloper.com/production/a-ludum-dare-postmortem-lessons-from-the-blitz- ; *Err Friday* (GMTK 2025, Godot). https://blazowacho.itch.io/err-friday/devlog/1003353/gmtk-game-jam-2025-post-mortem-when-everything-breaks-and-how-to-fix-it
- Guides jam : *Your First Game Jam: A Survival Guide* (Bugnet, 2026). https://bugnet.io/blog/your-first-game-jam-a-survival-guide ; *1-2-3-Scope Jam*. https://itch.io/jam/123scope-jam ; *Game Jam Scope Board*. https://czhchen.itch.io/game-jam-scope-board
