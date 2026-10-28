---
description: Mettre à jour ou installer les briques Tools Codex depuis marketplace et GitHub
argument-hint: [check] [--adopt] [--skills-dir CHEMIN] [--commands-dir CHEMIN]
---

Utilise le skill `tcu` pour cette demande `/TCU`. Exécute réellement son
script : sans argument de contrôle, applique ; avec `check` (ou `--check`),
contrôle sans écriture. `/tcu check` ne doit jamais lancer une application.
Installe systématiquement les plugins du catalogue officiel, les skills
autonomes et les commandes sources absents dans toutes les racines configurées.
Pour PROMPT, vérifie le skill et le résolveur embarqués avant son wrapper.
En contrôle seul, annonce ces installations sans les réaliser. Les conflits locaux restent
préservés et signalés sans bloquer les canaux indépendants.
Transmets les options fournies et ne force jamais une adoption. Rapporte
versions observées, sauvegardes, conflits et erreurs sans donnée sensible.

Cette commande source n'enregistre pas automatiquement une slash native.
Le skill est directement invocable avec `$tcu`.

Arguments reçus : `$ARGUMENTS`
