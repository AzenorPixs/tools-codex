## ADDED Requirements

### Requirement: Rafraîchissement planifié préalable distinct
Le planning utilisateur SHALL exécuter TFL avant PLLM normal et fournir son
catalogue frais explicitement. PLLM manuel SHALL continuer à lire son catalogue
sans lancer implicitement TFL. L'activité et le quota Codex SHALL conditionner
la séquence planifiée sans modifier les six politiques ou leurs contrôles.

#### Scenario: Commande manuelle ou séquence planifiée
- **WHEN** PLLM est invoqué manuellement ou après le TFL planifié réussi
- **THEN** il conserve ses six politiques et contrôles existants
- **AND** seule la séquence planifiée effectue le rafraîchissement préalable et les contrôles Codex
