# Design

## Context

Voir `proposal.md` pour la motivation. Les plugins `pllm` et `tfl` déclarent
actuellement chacun une version de build `0.1.0+codex.…`, sans version globale
de projet. Aucun fichier de version ni spécification principale n'existe.

## Goals / Non-Goals

**Goals:**

- Établir `VERSION` comme source de vérité de la version `0.2.0`.
- Conserver les métadonnées de build existantes dans les manifestes tout en
  alignant leur version de release sur `0.2.0`.
- Rendre la version immédiatement identifiable dans la documentation publique.

**Non-Goals:**

- Créer un tag, une release ou effectuer un push Git.
- Modifier les comportements fonctionnels des plugins, skills ou commandes.
- Modifier les données générées ou les dépendances.

## Decisions

- Utiliser un fichier texte `VERSION` contenant exclusivement `0.2.0` et une
  fin de ligne LF. Cette source est directement lisible sans dépendance ni
  format à interpréter. L'alternative consistant à choisir un manifeste de
  plugin comme source de vérité lierait la version du projet à un plugin et
  dupliquerait une responsabilité d'artefact.
- Déclarer `0.2.0` dans chaque manifeste de plugin sans suffixe de build. La
  version de release est alors strictement comparable à `VERSION`; la
  traçabilité de build reste assurée par l'historique de distribution plutôt
  que par une valeur différente dans les manifestes.
- Documenter la version dans `README.md`, puis préciser la responsabilité de
  `VERSION` dans `PROJECT.md` et `TECHNICAL.md`. Cela distingue la présentation
  publique du contrat technique de cohérence.

## Risks / Trade-offs

- [Des consommateurs dépendent du suffixe de build actuel] → la documentation
  signalera l'absence de changement fonctionnel; aucune migration automatique
  n'est nécessaire car les manifestes restent valides.
- [Une future release oublie un manifeste] → la spécification impose la
  vérification de tous les plugins publiés contre `VERSION`.

## Migration Plan

1. Ajouter `VERSION` avec `0.2.0`.
2. Aligner les deux manifestes publiés et la documentation.
3. Vérifier les JSON, l'égalité des versions et la validation OpenSpec stricte.

Le retour arrière consiste à rétablir la valeur de version précédente dans les
mêmes fichiers avant publication. Aucun effet externe n'est produit par ce
change.
