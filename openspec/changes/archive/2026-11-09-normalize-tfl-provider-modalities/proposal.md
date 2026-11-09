# TFL07 — Modalités fournisseurs résilientes dans TFL

## Why

La collecte TFL compare les libellés de modalités OpenCode Go et models.dev
comme des chaînes identiques. L’API peut publier des types MIME détaillés
(`image/jpeg`, `application/pdf`, `audio/mpeg`) alors que models.dev expose
leurs catégories (`image`, `pdf`, `audio`). Cette différence de granularité
bloque la collecte avant la publication des deux catalogues.

## What Changes

- Normaliser les types MIME connus en catégories communes avant les contrôles
  de cohérence et les filtres de sortie multimédia.
- Préserver les valeurs déclarées par chaque source, leur provenance et leurs
  dates dans l’audit JSON.
- Continuer à bloquer les déclarations réellement contradictoires, y compris
  les contradictions internes à une source ; préserver les valeurs inconnues
  sans inventer de catégorie.
- Garder la collecte dynamique pour les nouveaux modèles et les nouveaux
  fournisseurs, sans liste d’identifiants ni règle fondée sur leur nom.

## Impact

Les deux copies du script TFL, les tests de métadonnées Go, la spécification
`tfl-catalog`, la cartographie et le registre des lots, ainsi que le changelog.
Le test de parité des versions lit également la version courante dans `VERSION`
afin qu’un incrément CI/CD ne rende pas le test caduc. Pas de changement des
seuils, transports, tarifs, benchmarks, règles LM, formats de rapport ou dépendances.

## Validation

Tests hors ligne sur les deux distributions : équivalence MIME/catégorie,
préservation des valeurs sources, détection d’une contradiction réelle,
filtrage audio/vidéo de sortie après normalisation et absence de règle par nom.
Exécuter la suite ciblée TFL, la suite projet et les contrôles Python configurés,
avec le contrôle de parité des versions fondé sur `VERSION`, puis une collecte
TFL courante ; les refus d’accès des essais gratuits restent des échecs d’accès,
jamais des mesures inventées.
