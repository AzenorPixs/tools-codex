# TFL05 — Publier les sélections TFL vides sans bloquer les autres catalogues

## Why

TFL 0.7.9 arrête toute la collecte lorsqu'un catalogue valide ne contient
aucun modèle admissible. Les résultats des autres fournisseurs et les motifs
d'exclusion ne sont alors pas publiés. Le développeur a validé la correction
de ce comportement par SCM, avec incrément de la release commune à 0.7.10.

## What Changes

- Accepter une sélection vide avant ou après qualification des gratuits dans
  chacun des trois catalogues, y compris lorsque les trois sont vides.
- Publier les deux tableaux Go puis OpenRouter, avec une mention explicite
  et une synthèse des exclusions pour un tableau vide ; conserver le général
  uniquement dans le JSON et y indiquer son état.
- Publier les sources, compteurs, exclusions détaillées et essais gratuits
  courants sans réutiliser d'anciennes qualifications ; retourner zéro si les
  collectes sont valides et les rapports publiés.
- Préserver les filtres, les huit colonnes, les devises, les contrats CLI/JSON
  et les échecs bloquants sur les vraies erreurs de collecte ou de données.
- Synchroniser les deux distributions TFL, la documentation et la version.

## Impact

La sélection vide cesse d'être une erreur. Les consommateurs retrouvent
models sous forme de liste, éventuellement vide ; aucun modèle exclu n'est
réintégré. Le planning utilisateur reste inchangé et continue de refuser un
catalogue dont une section models est vide. Aucun appel fournisseur réel,
déploiement utilisateur, commit, push ou publication distante n'est inclus.

Les fichiers concernés sont les deux générateurs et SKILL.md TFL, leurs tests,
TECHNICAL.md, BUILD.md, README.md, CHANGELOG.md, VERSION, pyproject.toml et les
six manifestes plugins. AGENTS.md, PROJECT.md et DEVOPS.md restent applicables
sans changement. Le cycle inclut synchronisation, archivage et statistiques.
