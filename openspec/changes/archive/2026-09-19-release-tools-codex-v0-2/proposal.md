# Proposal

## Why

Tools Codex ne déclare pas de version de projet commune, alors que ses
plugins publiés portent chacun une version indépendante. La release 0.2.0
doit rendre cette version explicite et vérifiable dans les artefacts distribués.

## What Changes

- Ajouter une source de vérité de la version de projet à `0.2.0`.
- Aligner sur cette version les manifestes des plugins publiés `pllm` et `tfl`.
- Documenter la version de release dans la présentation publique du projet.
- **BREAKING** : aucune incompatibilité fonctionnelle ; seule la version publiée
  des plugins change.

## Capabilities

### New Capabilities

- `release-versioning`: définition et alignement vérifiable de la version de
  release publiée par Tools Codex et ses plugins.

### Modified Capabilities

- Aucun.

## Impact

- Ajout du fichier `VERSION`.
- Modification des manifestes `plugins/pllm/.codex-plugin/plugin.json` et
  `plugins/tfl/.codex-plugin/plugin.json`.
- Mise à jour de `README.md`, `PROJECT.md` et `TECHNICAL.md` pour documenter
  la version de projet et sa source de vérité.
- Aucun ajout de dépendance, appel réseau, commit, tag, publication ou push.
