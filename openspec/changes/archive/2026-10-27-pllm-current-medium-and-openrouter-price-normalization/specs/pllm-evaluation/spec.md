# Spec Delta

## ADDED Requirements

### Requirement: Effort courant séparé des traces historiques
PLLM SHALL valider l'effort demandé et mesuré dans l'évaluation courante sans traiter les métadonnées d'override ou d'anciennes tentatives comme son effort effectif. Les tentatives de performance courantes SHALL toujours établir Medium.

#### Scenario: Candidat Medium avec anciennes traces XHigh
- **WHEN** les capacités et les champs de requête et de mesure courants établissent Medium, mais que `user_override` ou `performance_attempts` historiques contiennent XHigh
- **THEN** PLLM conserve et évalue le candidat courant sans reprendre ces anciennes traces comme mesure ou palier valide

#### Scenario: Tentative courante non Medium
- **WHEN** la requête ou une tentative de performance de l'évaluation courante enregistre un effort autre que Medium
- **THEN** PLLM exclut le résultat courant malgré une capacité fournisseur qui inclut Medium
