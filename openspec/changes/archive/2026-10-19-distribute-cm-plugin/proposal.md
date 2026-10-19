## Why

Le catalogue CM est disponible comme skill autonome, mais la marketplace
Tools Codex ne propose que PLLM et TFL. Distribuer CM comme plugin permet de
le gérer par la même marketplace tout en conservant l'usage autonome.

## What Changes

- Ajouter `plugins/cm/.codex-plugin/plugin.json` et son skill embarqué
  `plugins/cm/skills/cm/SKILL.md`, sans script ni serveur MCP.
- Référencer `./plugins/cm` dans `.agents/plugins/marketplace.json`.
- Conserver `skills/cm/SKILL.md` et le lien local `.agents/skills/cm` ; adapter
  uniquement sa règle de maintenance pour garder les deux copies identiques.
- Porter la release commune de 0.2.2 à 0.2.3.
- Documenter les deux distributions et le risque de double entrée CM.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `extension-distribution` : plugin CM autonome et embarqué dans la marketplace.

## Impact

PROJECT, TECHNICAL, BUILD, README et CHANGELOG sont actualisés. VERSION,
pyproject.toml et les trois manifestes suivent la même release 0.2.3, selon
les invariants existants de release-versioning. Le catalogue CM conserve ses
trois invocations et ne déclenche aucun générateur. Les scripts PLLM/TFL,
leurs skills et les archives précédentes sont préservés.

Le périmètre autonome de spécification, implémentation, contrôles,
synchronisation, archivage et rapport est validé le 19 octobre 2026. La
publication distante et l'installation dans le profil Codex sont exclues de
cette livraison locale ; aucun état installé 0.2.3 n'est annoncé.
