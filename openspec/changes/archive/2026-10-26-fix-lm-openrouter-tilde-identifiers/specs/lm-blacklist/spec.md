## ADDED Requirements

### Requirement: Préfixe fournisseur OpenRouter marqué
LM SHALL accepter un unique `~` initial devant un segment fournisseur valide
suivi de `/`. Le marqueur SHALL disparaître avec le préfixe lors de la
canonicalisation. Les exclusions et validations existantes SHALL rester
applicables ; la limite de 256 caractères SHALL inclure le marqueur.

#### Scenario: Modèle autorisé avec préfixe marqué
- **WHEN** ~vendor/model est comparé à vendor/model ou model
- **THEN** leur identité canonique est identique et idempotente

#### Scenario: Exclusion marquée non contournable
- **WHEN** un identifiant marqué désigne un modèle exclu, avec casse ou suffixes gratuits
- **THEN** les exclusions par défaut, personnalisées et permanentes restent applicables
- **AND** les noms voisins restent distincts, sans recherche approximative

#### Scenario: Marqueur mal placé ou identifiant invalide
- **WHEN** un identifiant vaut ~model, ~~vendor/model ou vendor/~model, ou viole les limites ASCII existantes
- **THEN** il est rejeté avec un diagnostic sûr et sans mutation de la politique

#### Scenario: Persistance canonique
- **WHEN** LM ajoute ou retire ~vendor/model:free
- **THEN** il utilise la même entrée canonique que model et préserve les autres exclusions
