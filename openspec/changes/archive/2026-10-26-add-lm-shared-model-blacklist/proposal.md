# LM01 — Ajouter LM et une liste noire partagée

## Why
TFL et PLLM possèdent seulement des exclusions permanentes codées en dur.
Le développeur demande /LM pour gérer une liste commune, initialisée avec
mimo-v2.5, et écarter ces modèles de leurs sélections et tests.

## What Changes
- Ajouter LM : plugin, skill autonome/embarqué, commande source et découverte locale.
- Fournir LIST (défaut), ADD et REMOVE, stockage utilisateur commun atomique,
  validation stricte et correspondance des préfixes fournisseur/variantes gratuites.
- Filtrer TFL et PLLM avant sélection et génération, y compris forçages,
  catalogue ancien, mémoire, candidat direct et modes non visités.
- Ajouter LM à CM, qualifier TCU sans installation automatique de LM absent.
- Aligner la release locale sur 0.7.6, les six manifestes et les cadrages.

## Capabilities
### New Capabilities
- `lm-blacklist`: gestion et contrat de la liste noire commune.
### Modified Capabilities
- `tfl-catalog`: filtre LM avant qualification et publication.
- `pllm-evaluation`: filtre courant indépendant du catalogue et des historiques.
- `extension-distribution`: six plugins, LM et CM à jour.

## Impact
Sources skills/plugins LM/TFL/PLLM/CM, marketplace, commande LM, lien local,
tests de distribution et TCU, VERSION, pyproject.toml, PROJECT, TECHNICAL,
BUILD, README et CHANGELOG. Aucun nouveau service ni dépendance.
AGENTS et DEVOPS restent applicables sans modification. Pas de Git,
publication, installation utilisateur, accès fournisseur réel ou OpenCode.

## Autorisation
Périmètre autonome validé explicitement par le développeur le 26 octobre 2026,
avec rappel explicite de LM dans CM. Le cycle inclut spécification préalable,
implémentation, tests hors ligne, synchronisation, archivage et STATISTIQUES.md.
