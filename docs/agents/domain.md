# Documentation de domaine

Ce dépôt est configuré avec une documentation de domaine à contexte unique.

## Avant d’explorer le code

Lire :

- **`CONTEXT.md`** à la racine du dépôt, s’il existe ;
- les ADR de **`docs/adr/`** qui concernent la zone modifiée, s’ils existent.

Si ces fichiers n’existent pas, continuer sans signaler leur absence et sans proposer de les créer à l’avance. Le skill `/domain-modeling`, accessible via `/grill-with-docs` et `/improve-codebase-architecture`, les crée lorsque le vocabulaire du domaine ou une décision doit être réellement formalisé.

Si un `CONTEXT-MAP.md` est introduit plus tard pour passer à plusieurs contextes, lire ce fichier puis les `CONTEXT.md` et les ADR locaux pertinents.

## Organisation des fichiers

```text
/
├── CONTEXT.md
├── docs/
│   ├── agents/
│   └── adr/
└── src/
```

## Employer le vocabulaire du glossaire

Lorsqu’un livrable nomme un concept du domaine — titre de ticket, proposition de refactoring, hypothèse ou nom de test — employer le terme défini dans `CONTEXT.md` et éviter ses synonymes interdits.

Si le concept nécessaire n’est pas encore défini, deux possibilités existent :

- le vocabulaire est inventé et doit être reconsideré ;
- le domaine présente réellement une lacune, à signaler à `/domain-modeling`.

## Signaler les conflits avec les ADR

Si un livrable contredit un ADR existant, le signaler explicitement plutôt que de le remplacer silencieusement :

> _Contredit l’ADR-0007 (tickets pilotés par les événements), mais mérite d’être rouvert car…_
