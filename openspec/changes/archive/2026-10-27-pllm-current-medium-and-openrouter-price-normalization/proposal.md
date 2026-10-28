# PLL07 — Proposal

## Why

PLLM a rejeté le mode 1 alors que le candidat courant publiait Medium : des overrides et tentatives historiques en XHigh étaient parcourus comme s'ils décrivaient la requête courante. Le mode 5 a aussi exclu des candidats dont les prix flottants étaient une représentation binaire arrondie des mêmes prix décimaux TFL. Ces deux filtres empêchaient l'évaluation des candidats avant leurs tests de performance.

## What Changes

- Distinguer l'effort demandé et mesuré dans l'évaluation courante des métadonnées historiques d'override et de tentative.
- Accepter les valeurs flottantes équivalentes aux prix décimaux canoniques dans une tolérance relative stricte, tout en calculant classement et plafond depuis les prix décimaux exacts.
- Ajouter des tests de régression pour les deux cas et aligner la release locale sur 0.7.16, déjà déclarée dans les sources préparées.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `pllm-evaluation`: séparer les traces d'efforts historiques de la vérification des tentatives Medium courantes.
- `tfl-catalog`: tolérer uniquement l'écart de représentation flottante entre les prix numériques et leurs valeurs décimales canoniques, sans changer le classement exact ni le plafond.

## Impact

Le module `performance.py` partagé par les distributions autonomes et embarquées TFL/PLLM, leurs tests, `CHANGELOG.md`, `VERSION`, `pyproject.toml`, `README.md` et les six manifestes de plugin sont concernés. Aucun endpoint, seuil, protocole, secret, quota, palier ou comportement d'installation n'est modifié. L'évaluation réelle des fournisseurs reste distincte de la qualification hors ligne.
