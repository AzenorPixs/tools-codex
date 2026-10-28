# EXT04 — Exposer le catalogue CM comme skill découvrable

## Why

Le fichier `.codex/commands/cm.md` ne suffit pas à rendre `/cm` disponible
dans Codex. Le catalogue doit être exposé par un skill découvrable et
invocable avec `$cm`.

## What Changes

- Remplacer la commande source `/cm` par `skills/cm/SKILL.md` et le lien
  relatif `.agents/skills/cm` vers cette source unique.
- Afficher les invocations `$cm`, `$pllm` et `$tfl` avec leurs syntaxes et
  descriptions, en français, sans lancer PLLM ou TFL.
- **BREAKING** : supprimer `.codex/commands/cm.md` ; l'invocation devient `$cm`.
- Documenter la découverte dans le projet et l'installation autonome ailleurs.
- Porter la release commune de 0.2.1 à 0.2.2, sans publication externe.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `extension-distribution` : catalogue fourni par un skill et découverte locale.

## Impact

Les cadrages PROJECT, TECHNICAL et BUILD, le README et le CHANGELOG sont
actualisés. VERSION, pyproject.toml et les manifestes PLLM/TFL sont alignés.
Les invariants existants de `release-versioning` restent applicables sans
modification. Les sources PLLM/TFL, leurs scripts et la marketplace sont préservés.

Le périmètre autonome couvre la spécification, l'implémentation, les contrôles,
la synchronisation, l'archivage et son rapport. Il a été validé le 19 octobre
2026 avant toute écriture. Aucun commit, push, accès fournisseur, installation
globale ou changement d'infrastructure n'est inclus.
