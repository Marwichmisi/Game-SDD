# Suivi des tickets : GitHub

Les tickets et spécifications de ce dépôt sont conservés dans GitHub Issues. Utiliser la CLI `gh` pour toutes les opérations.

## Conventions

- **Créer un ticket** : `gh issue create --title "..." --body "..."`. Utiliser un heredoc pour un corps multiligne.
- **Lire un ticket** : `gh issue view <numéro> --comments`, en filtrant les commentaires avec `jq` et en récupérant également les étiquettes.
- **Lister les tickets** : `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` avec les filtres `--label` et `--state` appropriés.
- **Commenter un ticket** : `gh issue comment <numéro> --body "..."`.
- **Ajouter ou retirer une étiquette** : `gh issue edit <numéro> --add-label "..."` ou `gh issue edit <numéro> --remove-label "..."`.
- **Fermer un ticket** : `gh issue close <numéro> --comment "..."`.

Déduire le dépôt à partir de `git remote -v` ; `gh` le fait automatiquement depuis un clone.

## Pull requests comme surface de triage

**PRs comme surface de triage : non.** _(Passer à `yes` si ce dépôt traite les PR externes comme des demandes de fonctionnalités ; `/triage` lit ce drapeau.)_

Lorsque la valeur est `yes`, les PR suivent les mêmes étiquettes et les mêmes états que les tickets, avec les commandes `gh pr` équivalentes :

- **Lire une PR** : `gh pr view <numéro> --comments` et `gh pr diff <numéro>` pour le diff.
- **Lister les PR externes à trier** : `gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`, puis ne conserver que les associations `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR` ou `NONE` (exclure `OWNER`, `MEMBER` et `COLLABORATOR`).
- **Commenter, étiqueter ou fermer** : `gh pr comment`, `gh pr edit --add-label` / `--remove-label`, `gh pr close`.

GitHub partage un espace de numérotation entre les tickets et les PR. Une référence comme `#42` peut donc désigner l’un ou l’autre : tenter `gh pr view 42`, puis `gh issue view 42`.

## Quand un skill demande de publier dans le suivi des tickets

Créer un ticket GitHub.

## Quand un skill demande de récupérer le ticket pertinent

Exécuter `gh issue view <numéro> --comments`.

## Opérations de cartographie

Utilisées par `/wayfinder`. La **carte** est un ticket unique dont les tickets enfants sont les unités de travail.

- **Carte** : un ticket étiqueté `wayfinder:map`, contenant les notes, décisions prises et zones encore inconnues. Créer le ticket avec `gh issue create --label wayfinder:map`.
- **Ticket enfant** : un ticket lié à la carte comme sous-ticket GitHub (`gh api` sur l’endpoint des sous-tickets). Si les sous-tickets ne sont pas activés, ajouter l’enfant à une liste de tâches dans le corps de la carte et indiquer `Part of #<carte>` au début du corps de l’enfant. Étiquettes : `wayfinder:<type>` (`research`, `prototype`, `grilling` ou `task`). Une fois pris en charge, le ticket est assigné au développeur qui le pilote.
- **Blocage** : utiliser de préférence les dépendances natives entre tickets GitHub, qui constituent la représentation canonique visible dans l’interface. Ajouter une arête avec `gh api --method POST repos/<propriétaire>/<dépôt>/issues/<ticket-enfant>/dependencies/blocked_by -F issue_id=<id-base-du-bloquant>`, où `<id-base-du-bloquant>` est l’identifiant numérique de base de données du bloquant (`gh api repos/<propriétaire>/<dépôt>/issues/<numéro> --jq .id`, et non le `#numéro` ni le `node_id`). Si les dépendances ne sont pas disponibles, ajouter `Blocked by: #<numéro>, #<numéro>` au début du corps de l’enfant. Un ticket est débloqué lorsque tous ses bloquants sont fermés.
- **Recherche du front** : lister les enfants ouverts de la carte (`gh issue list --state open`, limité à ses sous-tickets ou à sa liste de tâches), retirer ceux qui ont un bloquant ouvert (`issue_dependencies_summary.blocked_by > 0`, ou un ticket ouvert dans la ligne `Blocked by`) ou un assigné ; le premier dans l’ordre de la carte gagne.
- **Prise en charge** : `gh issue edit <numéro> --add-assignee @me`, première écriture de la session.
- **Résolution** : `gh issue comment <numéro> --body "<réponse>"`, puis `gh issue close <numéro>`, puis ajouter un pointeur de contexte dans les décisions de la carte.
