---
description: Mettre à jour les briques Tools Codex installées depuis marketplace et GitHub
argument-hint: [check] [--adopt] [--skills-dir CHEMIN] [--commands-dir CHEMIN]
---

Utilise le skill `tcu` pour cette demande `/TCU`. Exécute réellement son
script : sans argument de contrôle, applique ; avec `check` (ou `--check`),
contrôle sans écriture. `/tcu check` ne doit jamais lancer une application.
Le composant prompt absent est le seul installé automatiquement : plugin,
skill embarqué vérifié et wrapper de commande. Les conflits locaux restent
préservés et signalés sans bloquer les canaux indépendants.
Transmets les options fournies et ne force jamais une adoption. Rapporte
versions observées, sauvegardes, conflits et erreurs sans donnée sensible.

Cette commande source n'enregistre pas automatiquement une slash native.
Le skill est directement invocable avec `$tcu`.

Arguments reçus : `$ARGUMENTS`
