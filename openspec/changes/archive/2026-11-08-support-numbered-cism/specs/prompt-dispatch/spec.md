## ADDED Requirements

### Requirement: Variantes CISM numérotées directes
Le dispatcher SHALL accepter CISMx et 1CISMx pour tout entier décimal ASCII strictement positif sans zéro initial, sans borne ni conversion numérique. Il SHALL résoudre CISM.md depuis le référentiel du projet et préserver le numéro exact sous la forme CISMn.

#### Scenario: Cycle normal
- **WHEN** CISM10 est invoqué
- **THEN** le RUN CISM10 est transmis sans limite de change

### Requirement: Cycle direct limité
La variante 1CISMx SHALL limiter le cycle à un change, son archivage et ses statistiques, puis arrêter la session de codage. Le mode direct SHALL NOT activer le pilotage CAB. Les arguments invalides SHALL être refusés avant toute lecture de configuration.

#### Scenario: Un change direct
- **WHEN** 1CISM10 est invoqué
- **THEN** le dispatcher sélectionne CISM.md avec le RUN CISM10 et une limite d'un change

#### Scenario: Numéro long et invalide
- **WHEN** CISM suivi de 5000 chiffres ASCII valides est fourni
- **THEN** chaque chiffre est conservé et aucune limite de change n'est ajoutée
- **AND** un suffixe nul, signé, non ASCII ou avec zéro initial est refusé
