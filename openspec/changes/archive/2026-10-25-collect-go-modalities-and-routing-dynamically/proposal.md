# Métadonnées Go dynamiques dans TFL

## Why

Les modalités et routes Go utilisent encore des listes statiques de modèles.
MiniMax-M3.1-Flash reste ainsi non vérifié malgré des métadonnées publiées.
Le développeur valide leur collecte automatique sans listes de modèles,
le cycle SCM/OpenSpec complet et la release finale 0.5.5.

## What Changes

- Collecter les modalités et le transport Go depuis l'API et models.dev,
  avec provenance par champ, sans liste de noms ou de familles de modèles.
- Résoudre les trois protocoles déjà consommés par PLLM depuis des métadonnées
  explicites de protocole/SDK et une base API publiée, jamais depuis l'ID.
- Supprimer les tables statiques de modalités et de routage dans TFL.
- Conserver l'inconnu explicite et bloquer les contradictions ou les données
  indispensables invalides avant publication ; ne jamais inventer un protocole.
- Vérifier les URL avant de les publier aux consommateurs qui portent des
  secrets ; aucune route de source distante ne peut déplacer l'origine HTTPS.
- Synchroniser les deux distributions, les documents et la release 0.5.5.

## Impact

Scripts et SKILL.md TFL autonomes et embarqués, tests tarifaires existants et
nouvelle suite tests/test_tfl_go_metadata.py, README, TECHNICAL, BUILD,
CHANGELOG, VERSION, pyproject.toml, cinq manifestes et spec tfl-catalog.
Pas de modification du moteur PLLM, de son quota, du profil utilisateur,
des archives précédentes, de Git ou des dépendances.

## Validation

Périmètre et cycle OpenSpec explicitement validés par le développeur le
25 octobre 2026 avant création de ce change. Les tests hors ligne des deux
distributions couvrent le nouveau modèle, les modalités multimédias, les
protocoles reconnus/inconnus, les priorités, les contradictions, l'URL et la
préservation des rapports. Qualification Python 3.13/3.14 et collecte réelle
des seules métadonnées, sans génération de tokens ni benchmark PLLM.
