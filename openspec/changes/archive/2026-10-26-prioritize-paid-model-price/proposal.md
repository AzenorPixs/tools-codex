## Why

PLLM retient actuellement le débit maximal après qualification. Cela peut
sélectionner un payant plus cher alors qu'un modèle moins cher satisfait tous
les critères. Le développeur exige que le prix établisse le classement des
payants admissibles ; les gratuits restent classés par performances.

## What Changes

- Classer les payants valides des modes 1/2 et de la catégorie payante de 5
  par coût moyen TFL croissant ; départager les prix égaux par débit
  décroissant, TTFT croissant puis ordre TFL stable.
- Garder les performances pour les gratuits 3/4 et le repli gratuit de 5.
- Conserver tous les contrôles, les priorités 1 à 6, les forçages et le
  protocole 8 ; publier le prix utilisé dans les preuves JSON.
- Aligner les deux distributions PLLM, les instructions et la documentation.
- Incrémenter la release commune 0.7.3 vers 0.7.4, à la demande complémentaire
  explicite du développeur, avec les cinq manifestes et la métadonnée Python.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `pllm-evaluation` : classement des payants par prix après qualification.

## Impact

Les scripts et skills PLLM autonomes/embarqués, le wrapper PLLM, leurs tests,
TECHNICAL.md, BUILD.md, README.md et CHANGELOG.md sont concernés. TFL fournit
déjà les prix requis et reste inchangé. Aucun changement des secrets,
dépendances, installations utilisateur, agents OpenCode ou priorités entre
politiques. Le changement est réversible dans les sources ; les nouvelles
évaluations restent datées et ne réécrivent pas les anciennes mesures.

## Autorisation et validation

Le développeur a demandé le change SCM, précisé séparément le classement des
payants et des gratuits, puis demandé de rejouer immédiatement PLLM avec cette
règle après présentation du périmètre. Le périmètre comprend la spécification,
l'implémentation, les tests, la documentation et l'archivage du seul change.
Le développeur a ensuite demandé explicitement l'incrément des briques.
La nouvelle évaluation réelle est explicitement demandée ; l'installation et
la publication distante restent des opérations distinctes.
