# SDD Godot

Système de développement piloté par agents pour jeux Godot 4.x, du concept au publish : une fondation intacte, une couche jeu adaptée, un workflow à gates.

## Language

**Noyau**:
La fondation prouvée conservée intacte et jamais éditée.
_Avoid_: core, upstream

**Couche jeu**:
L'ensemble des adaptations et ajouts spécifiques Godot construits par-dessus le Noyau.
_Avoid_: couche Godot, game layer

**Map**:
La carte de travail qui ordonne les décisions et les tickets vers la spec.
_Avoid_: carte, roadmap

**Surcharge**:
Une adaptation qui conserve le processus du Noyau et réécrit seulement les contrôles et exemples pour Godot.
_Avoid_: fork, override

**Addenda**:
Un skill nouveau créé pour couvrir un manque du Noyau propre au jeu.
_Avoid_: add-on, extension

**Vertical slice**:
Une construction de production à fidélité shipping qui traverse tout le pipeline et conditionne l'entrée en production.
_Avoid_: démo, prototype avancé

**Playtest**:
La boucle hypothèse → session → synthèse → action qui pilote l'itération.
_Avoid_: QA, test salon
