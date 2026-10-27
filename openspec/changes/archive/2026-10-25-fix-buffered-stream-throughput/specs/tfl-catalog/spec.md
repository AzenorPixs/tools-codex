## MODIFIED Requirements

### Requirement: Métadonnées auditables
Le JSON TFL SHALL conserver sources, exclusions et routage sans secret.
Les essais gratuits SHALL tracer critères, niveau, tentatives, comptages,
profil, formule et durée totale non arrondie. Le débit SHALL employer le même
moteur et la même durée complète que PLLM. Une mesure historique SHALL NOT
valider une collecte actuelle. Le rapport SHALL préciser que le débit moyen
inclut l'attente et le TTFT.

#### Scenario: Consultation du routage d'un modèle OpenCode Go
- **WHEN** un consommateur examine un modèle retenu du catalogue
- **THEN** il retrouve les champs de routage et leurs sources sans déduire le protocole du seul nom commercial


#### Scenario: Qualification gratuite avec réception en rafale
- **WHEN** un gratuit fournit sa réponse par fragments groupés
- **THEN** la qualification applique les seuils au débit moyen sur la requête complète
- **AND** les mesures non fiables sont exclues avec cause, sans écrêtage artificiel
