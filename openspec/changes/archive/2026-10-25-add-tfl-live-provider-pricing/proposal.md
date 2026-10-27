# Actualisation automatique des tarifs TFL

## Why

La table tarifaire statique OpenCode Go omet des modèles disponibles et peut
conserver des prix anciens. OpenRouter collecte déjà ses prix via son API,
mais la provenance tarifaire et la date de récupération doivent être explicites.

## What Changes

- Collecter les tableaux tarifaires officiels OpenCode Go à chaque génération,
  sans repli sur la table statique ni sur un catalogue antérieur.
- Associer les noms publiés aux identifiants disponibles sans correspondance
  approximative ; conserver les variantes et les motifs d'exclusion.
- Conserver la collecte API OpenRouter et tracer la source et la date des
  tarifs des deux fournisseurs, y compris les prix de cache disponibles.
- Préserver les filtres, les identifiants OpenRouter, les colonnes et les CLI.
- Aligner VERSION, pyproject.toml, README et les cinq plugins sur 0.5.2.

## Impact

Sources autonome et embarquée TFL, tests hors ligne, documentation technique
et de distribution, spécification tfl-catalog et métadonnées de release.
Aucune dépendance supplémentaire, installation de profil ni opération Git.
Les lectures HTTPS officielles et une collecte de qualification locale sont
autorisées par le périmètre SCM validé par le développeur le 25 octobre 2026.

## Validation

Périmètre autonome, création, synchronisation et archivage explicitement
validés par le développeur avant toute écriture de code ou de tests.
Les tests doivent établir le rafraîchissement, les variantes tarifaires,
les erreurs et la préservation des rapports ; une collecte réelle complète
doit être distinguée de la qualification hors ligne et de l'installation.
