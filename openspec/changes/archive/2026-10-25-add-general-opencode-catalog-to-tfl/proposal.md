# Catalogue général OpenCode dans TFL

## Why

TFL couvre Go et OpenRouter mais pas le catalogue général OpenCode. Le
développeur demande son ajout avec contexte ≥ 1M et coût moyen ≤ 0,50 USD/M,
cycle SCM/OpenSpec complet et incrément de release 0.0.1, soit 0.5.6 depuis
l'état initial 0.5.5.

## What Changes

- Ajouter une collecte distincte du catalogue général et de ses tarifs officiels.
- Lire ses métadonnées dans le fournisseur models.dev opencode, sans reprendre
  les limites, tarifs ou routes de opencode-go pour un même identifiant.
- Ajouter le tableau général entre Go et OpenRouter, avec huit colonnes communes.
- Conserver les seuils et filtres, prix gratuits vérifiés inclus, ainsi que la
  blacklist OpenCode existante et les motifs d'exclusion.
- Conserver les sections JSON Go/OpenRouter et ajouter opencode ; ne pas
  étendre le moteur PLLM ni ses politiques à cette nouvelle section.
- Mettre à jour les consignes, wrapper et descriptions CM/TFL devenues incomplètes,
  les cadrages concernés et la release commune 0.5.6 des cinq plugins.

## Impact

Deux distributions TFL, tests existants et tests/test_tfl_opencode_catalog.py,
consignes CM autonome/embarquées, wrapper .codex/commands/tfl.md, PROJECT,
TECHNICAL, BUILD, README, CHANGELOG, VERSION, pyproject.toml, cinq manifestes
et spec tfl-catalog. Aucun ancien change, moteur PLLM, profil, Git ou dépendance.

## Validation

Demande explicite du développeur autorisant l'évolution et le cycle OpenSpec.
Critères : catalogue complet indépendant, limites 1M/0,50 incluses, exclusion
des variantes gratuites 200K, séparation des tarifs et routes, colonnes et
ordre des trois tableaux, erreurs sans publication partielle et compatibilité
de lecture des sections existantes. Qualification hors ligne Python 3.13/3.14
et collecte réelle dans un temporaire du projet, sans génération ni quotas.
