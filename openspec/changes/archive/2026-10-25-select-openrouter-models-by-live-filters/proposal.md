# Sélection dynamique OpenRouter

## Why

TFL actualise les tarifs OpenRouter mais limite encore la sélection à trois
identifiants. Cette liste empêche l'apparition automatique d'autres modèles
admissibles. Le développeur a validé un complément SCM, cycle OpenSpec compris,
pour filtrer tout le catalogue API et a demandé la version finale 0.5.3.

## What Changes

- Interroger l'intégralité du catalogue OpenRouter sans filtre de catégorie,
  modalité ou plafond de nombre de modèles dans la requête.
- Examiner chaque modèle selon les seuils existants de contexte, coût,
  modalités de sortie et blacklist, sans liste d'identifiants admissibles.
- Admettre les prix gratuits vérifiés et exclure les prix inconnus, négatifs,
  non finis ou supérieurs au seuil avec un motif explicite.
- Supprimer l'erreur provoquée par l'absence d'un ancien identifiant fixé.
- Préserver la collecte Go, les colonnes, CLI, prix API de base et provenance.
- Aligner les métadonnées de release et les cinq plugins sur 0.5.3.

## Impact

Deux distributions TFL (script et SKILL.md), fixtures et tests tarifaires,
README, TECHNICAL, BUILD, CHANGELOG, VERSION, pyproject.toml, manifestes et
spécification tfl-catalog. Aucun fichier de profil, ancien change archivé,
Git, dépendance ou service ne sera modifié.

## Validation

Périmètre fonctionnel et cycle autonome OpenSpec validés explicitement par le
développeur le 25 octobre 2026, avant toute écriture de code ou de tests.
Critères : modèle inédit admissible retenu, modèle hors seuil exclu, disparition
d'un ancien modèle sans échec, requête non restreinte, audit des exclusions,
publication déterministe et compatibilité de la provenance. Qualification
hors ligne sur les deux distributions et Python 3.13/3.14, puis collecte réelle
dans un répertoire temporaire du projet. L'installation de profil est distincte.
